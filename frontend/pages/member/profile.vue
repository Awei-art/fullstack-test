<script setup>
import { ref, reactive, onMounted, computed } from 'vue';

definePageMeta({
  layout: 'default',
  middleware: 'auth'
});

const config = useRuntimeConfig();
const userCookie = useCookie('user_info');
const isLoading = ref(true);
const isSaving = ref(false);
const saveMessage = ref('');
const errorMessage = ref('');

// 使用者低風險的編輯欄位
const form = reactive({
  nickname: '',
  gender: 'O',
  birthMonth: '',
  birthDay: '',
  accept_promotions: true
});

// 月份與日期邏輯
const months = Array.from({ length: 12 }, (_, i) => {
  const m = i + 1;
  return m < 10 ? '0' + m : '' + m;
});

const daysInMonth = computed(() => {
  if (!form.birthMonth) return [];
  const month = parseInt(form.birthMonth);
  let days = 31;
  if ([4, 6, 9, 11].includes(month)) days = 30;
  if (month === 2) days = 29; // 不考慮年份，2月允許到29日
  
  return Array.from({ length: days }, (_, i) => {
    const d = i + 1;
    return d < 10 ? '0' + d : '' + d;
  });
});

// 抓取現有資料
const fetchMemberData = async () => {
  const token = userCookie.value?.token;
  if (!token) return navigateTo('/login');

  try {
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    const realData = await $fetch('/profile/', {
      baseURL: baseURL,
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (realData) {
      form.nickname = realData.nickname || '';
      // 如果沒有暱稱，可以嘗試把原生 firstname 或 username 當作預設顯示
      if (!form.nickname && realData.first_name) {
          form.nickname = realData.first_name;
      } else if (!form.nickname && realData.username && !realData.username.startsWith('google_') && !realData.username.startsWith('line_')) {
          form.nickname = realData.username;
      }

      form.gender = realData.gender || 'O';
      
      if (realData.birth_month_day && realData.birth_month_day.length === 4) {
          form.birthMonth = realData.birth_month_day.substring(0, 2);
          form.birthDay = realData.birth_month_day.substring(2, 4);
      }
      
      form.accept_promotions = realData.accept_promotions !== undefined ? realData.accept_promotions : true;
    }
  } catch (err) {
    if (err.response?.status === 401 || err.data?.statusCode === 401) {
      userCookie.value = null;
      navigateTo('/login');
    }
  } finally {
    isLoading.value = false;
  }
};

// 儲存資料
const handleSave = async () => {
  if (isSaving.value) return;
  isSaving.value = true;
  saveMessage.value = '';
  errorMessage.value = '';

  const token = userCookie.value?.token;
  try {
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    
    // 組合出生月日
    const birth_month_day = (form.birthMonth && form.birthDay) ? `${form.birthMonth}${form.birthDay}` : null;
    
    const response = await $fetch('/profile/', {
      baseURL: baseURL,
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` },
      body: {
        nickname: form.nickname,
        gender: form.gender,
        birth_month_day: birth_month_day,
        accept_promotions: form.accept_promotions
      }
    });

    if (response) {
      saveMessage.value = '資料已經更新完畢！';
      
      // 更新 Cookie 的顯示名稱為暱稱，讓右上角 Header 能夠即時更改
      if (form.nickname && userCookie.value) {
         userCookie.value = {
            ...userCookie.value,
            username: form.nickname
         };
      }
    }
  } catch (err) {
    errorMessage.value = err.data?.error || '儲存失敗，請稍後再試。';
  } finally {
    isSaving.value = false;
    setTimeout(() => { saveMessage.value = '' }, 3000);
  }
};

onMounted(() => {
  fetchMemberData();
});
</script>

<template>
  <div class="member-page-container">
    <div class="content-wrapper">
      <!-- Left Sidebar -->
      <MemberSidebar />

      <!-- Right Dashboard Content -->
      <main class="dashboard-content">
        <div class="member-banner">
          <div class="banner-info">
            <h1 class="welcome-text">會員基本資料</h1>
            <p class="join-date">在這裡管理您的個人資歷</p>
          </div>
        </div>

        <!-- 🔥 載入中畫面 -->
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>載入中...</p>
        </div>

        <template v-else>
          <div class="info-grid">
             <div class="info-card" style="grid-column: 1 / -1; max-width: 600px;">
                <div class="card-header">
                  <h3>編輯您的基本資料</h3>
                </div>
                <div class="card-body">
                  <form @submit.prevent="handleSave" class="profile-form">
                    
                    <!-- 1. 暱稱 -->
                    <div class="form-group">
                      <label class="form-label">顯示暱稱</label>
                      <input 
                        v-model="form.nickname" 
                        type="text" 
                        class="form-input" 
                        placeholder="請輸入您希望大家怎麼稱呼您" 
                        :disabled="isSaving"
                        maxlength="50"
                      />
                      <span class="input-hint">這會顯示在網站右上角，以及任何公開評論區中。</span>
                    </div>

                    <!-- 2. 性別稱謂 Dropdown -->
                    <div class="form-group">
                      <label class="form-label">稱謂 (性別)</label>
                      <select v-model="form.gender" class="form-input form-select" :disabled="isSaving">
                        <option value="O">保密</option>
                        <option value="M">男性</option>
                        <option value="F">女性</option>
                      </select>
                    </div>
                    
                    <!-- 3. 出生月日 (兩個 Dropdown) -->
                    <div class="form-group">
                      <label class="form-label">出生月日</label>
                      <div class="birthday-inputs">
                        <select v-model="form.birthMonth" class="form-input form-select" :disabled="isSaving" @change="form.birthDay = ''">
                          <option value="">選擇月份</option>
                          <option v-for="m in months" :key="m" :value="m">{{ m }} 月</option>
                        </select>
                        <select v-model="form.birthDay" class="form-input form-select" :disabled="isSaving || !form.birthMonth">
                          <option value="">選擇日期</option>
                          <option v-for="d in daysInMonth" :key="d" :value="d">{{ parseInt(d) }} 日</option>
                        </select>
                      </div>
                      <span class="input-hint">我們將在您的生日月份寄送驚喜專屬禮！</span>
                    </div>

                    <!-- 4. 接受優惠通知意願 Toggle/Checkbox -->
                    <div class="form-group toggle-group" style="padding-top: 10px;">
                      <label class="checkbox-container">
                        <input type="checkbox" v-model="form.accept_promotions" :disabled="isSaving" />
                        <span class="checkmark"></span>
                        <div class="checkbox-text">
                            <strong>我願意接收優惠通知</strong>
                            <p>獲取田園葡萄最新產品、折價券與專屬活動消息，隨時可關閉。</p>
                        </div>
                      </label>
                    </div>
  
                    <!-- 訊息顯示區 -->
                    <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
                    <div v-if="saveMessage" class="success-msg">
                       <svg xmlns="http://www.w3.org/2000/svg" class="success-icon" viewBox="0 0 20 20" fill="currentColor">
                         <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                       </svg>
                       {{ saveMessage }}
                    </div>
  
                    <!-- 儲存按鈕 -->
                    <div class="form-actions">
                      <button type="submit" class="submit-btn" :disabled="isSaving">
                        <span v-if="isSaving" class="spinner-small"></span>
                        {{ isSaving ? '儲存中...' : '儲存變更' }}
                      </button>
                    </div>
                    
                  </form>
                </div>
              </div>
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<style src="@/assets/css/Member_page.css" scoped></style>
<style scoped>
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: #444;
}

.input-hint {
  font-size: 12px;
  color: #888;
  margin-top: 2px;
}

/* 輸入框設計 */
.form-input {
  padding: 12px 16px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  font-size: 15px;
  color: #333;
  transition: all 0.2s;
  background-color: #fcfcfc;
  width: 100%;
}

.form-input:focus {
  border-color: #C1A96C;
  outline: none;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(193, 169, 108, 0.15);
}

.form-input:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
  opacity: 0.7;
}

.form-select {
  appearance: none;
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2220%22%20height%3D%2220%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M5%208l5%205%205-5%22%20stroke%3D%22%23999%22%20stroke-width%3D%222%22%20fill%3D%22none%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 40px;
}

/* 生日組合 */
.birthday-inputs {
  display: flex;
  gap: 12px;
}
.birthday-inputs .form-input {
  flex: 1;
}

/* Checkbox (優惠通知) 設計 */
.checkbox-container {
  display: flex;
  align-items: flex-start;
  position: relative;
  padding-left: 28px;
  cursor: pointer;
  user-select: none;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 3px;
  left: 0;
  height: 20px;
  width: 20px;
  background-color: #fff;
  border: 1px solid #c4c4c4;
  border-radius: 4px;
  transition: all 0.2s;
}

.checkbox-container:hover input ~ .checkmark {
  border-color: #C1A96C;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #C1A96C;
  border-color: #C1A96C;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.checkbox-text strong {
  font-size: 15px;
  color: #333;
}

.checkbox-text p {
  font-size: 13px;
  color: #888;
  margin: 0;
}

/* 按鈕與訊息 */
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.submit-btn {
  background-color: #C1A96C;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.submit-btn:hover:not(:disabled) {
  background-color: #b0985c;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background-color: #d3d3d3;
  cursor: not-allowed;
  transform: none;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-msg {
  color: #E25E5E;
  font-size: 14px;
  background-color: #FEE2E2;
  padding: 10px 14px;
  border-radius: 6px;
  margin-top: 5px;
}

.success-msg {
  color: #2F8A3B;
  font-size: 14px;
  background-color: #E8F5E9;
  padding: 10px 14px;
  border-radius: 6px;
  margin-top: 5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.success-icon {
  width: 18px;
  height: 18px;
}
</style>
