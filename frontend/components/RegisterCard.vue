<script setup>
import { reactive, ref } from 'vue';

// 取得 API 設定
const config = useRuntimeConfig();

// 路由控制 (返回首頁)
const router = useRouter();
const goBack = () => {
  router.push('/');
};

// 表單資料
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// 錯誤訊息 (API 返回的全局錯誤)
const errorMessage = ref('');

// 欄位即時驗證錯誤訊息
const fieldErrors = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

// 即時驗證函式
const validateUsername = () => {
  if (!form.username) {
    fieldErrors.username = '';
    return;
  }
  const usernameRegex = /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
  if (form.username.length < 8) {
    fieldErrors.username = '帳號必須至少 8 碼';
  } else if (!usernameRegex.test(form.username)) {
    fieldErrors.username = '帳號必須包含英文與數字混合，不可含有特殊符號';
  } else {
    fieldErrors.username = '';
  }
};

const validatePassword = () => {
  if (!form.password) {
    fieldErrors.password = '';
    return;
  }
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  if (form.password.length < 8) {
    fieldErrors.password = '密碼必須至少 8 碼';
  } else if (!/(?=.*[A-Z])/.test(form.password)) {
    fieldErrors.password = '密碼必須包含至少 1 個大寫英文';
  } else if (!/(?=.*[a-z])/.test(form.password)) {
    fieldErrors.password = '密碼必須包含至少 1 個小寫英文';
  } else if (!/(?=.*\d)/.test(form.password)) {
    fieldErrors.password = '密碼必須包含至少 1 個數字';
  } else {
    fieldErrors.password = '';
  }
  
  if (form.confirmPassword) {
    validateConfirmPassword();
  }
};

const validateConfirmPassword = () => {
  if (!form.confirmPassword) {
    fieldErrors.confirmPassword = '';
    return;
  }
  if (form.password !== form.confirmPassword) {
    fieldErrors.confirmPassword = '兩次密碼輸入不一致';
  } else {
    fieldErrors.confirmPassword = '';
  }
};

// 載入狀態
const isLoading = ref(false);

// 註冊處理函式
const handleRegister = async () => {
  // 防止重複點擊
  if (isLoading.value) return;

  // 清空錯誤訊息
  errorMessage.value = '';

  // 執行即時驗證檢查是否有錯
  validateUsername();
  validatePassword();
  validateConfirmPassword();

  if (fieldErrors.username || fieldErrors.password || fieldErrors.confirmPassword) {
    errorMessage.value = '請修正欄位下方的錯誤後再送出';
    return;
  }

  try {
    isLoading.value = true;

    // 3. 發送註冊請求給 Django
    // 這裡使用 /register/ 並指定 baseURL，以便在 client/server 之間正確切換
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    const { data, error } = await useFetch('/register/', {
      baseURL: baseURL,
      method: 'POST',
      body: {
        username: form.username,
        email: form.email,
        password: form.password
      }
    });

    // 4. 處理錯誤
    if (error.value) {
      console.error('註冊失敗:', error.value);

      // 根據錯誤狀態碼顯示不同訊息
      if (error.value.statusCode === 400) {
        // Django 回傳的詳細錯誤訊息
        const errorData = error.value.data;
        
        if (errorData?.username) {
          errorMessage.value = '此帳號已被使用';
        } else if (errorData?.email) {
          errorMessage.value = '此 Email 已被註冊';
        } else {
          errorMessage.value = '註冊失敗，請檢查輸入格式';
        }
      } else {
        // 可以直接顯示後端傳來的詳細 errorMessage
        if (error.value.data && typeof error.value.data === 'object') {
             // 拿取第一個欄位的錯誤作為錯誤訊息
             const firstKey = Object.keys(error.value.data)[0];
             errorMessage.value = error.value.data[firstKey][0];
        } else {
             errorMessage.value = '註冊失敗，請稍後再試';
        }
      }
      return;
    }

    // 5. 註冊成功
    if (data.value) {
      console.log('註冊成功:', data.value);
      
      // 跳轉到登入頁
      await navigateTo('/login?registered=true');
    }

  } catch (err) {
    console.error('系統錯誤:', err);
    errorMessage.value = '系統連線錯誤，請檢查網路後再試';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login_wrapper">
    <div class="login_card">
      <!-- 返回按鈕 -->
      <button @click="goBack" class="back-btn">
        <svg xmlns="http://www.w3.org/2000/svg" class="back-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        返回
      </button>

      <!-- 標題 -->
      <div class="login_header">
        <img src="/images/logo_icon.svg" alt="Logo" class="login_logo">
        <h2>加入會員</h2>
      </div>

      <!-- 註冊表單 -->
      <form @submit.prevent="handleRegister" class="login_form">
        
        <!-- 錯誤訊息 -->
        <div v-if="errorMessage" class="error_alert">
          <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          {{ errorMessage }}
        </div>

        <!-- 帳號 -->
        <div class="input_group">
          <input 
            v-model="form.username" 
            @input="validateUsername"
            @blur="validateUsername"
            type="text" 
            placeholder="請輸入帳號（8碼以上，英數混合）" 
            required
            :disabled="isLoading"
            :class="{ 'has-error': fieldErrors.username }"
          >
          <div v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</div>
        </div>

        <!-- 密碼 -->
        <div class="input_group">
          <input 
            v-model="form.password" 
            @input="validatePassword"
            @blur="validatePassword"
            type="password" 
            placeholder="設定密碼（8碼以上，須含大小寫英文與數字）" 
            required
            :disabled="isLoading"
            :class="{ 'has-error': fieldErrors.password }"
          >
          <div v-if="fieldErrors.password" class="field-error">{{ fieldErrors.password }}</div>
        </div>

        <!-- 確認密碼 -->
        <div class="input_group">
          <input 
            v-model="form.confirmPassword"
            @input="validateConfirmPassword"
            @blur="validateConfirmPassword"
            type="password" 
            placeholder="再次確認密碼" 
            required
            :disabled="isLoading"
            :class="{ 'has-error': fieldErrors.confirmPassword }"
          >
          <div v-if="fieldErrors.confirmPassword" class="field-error">{{ fieldErrors.confirmPassword }}</div>
        </div>

        <!-- Email -->
        <div class="input_group">
          <input 
            v-model="form.email" 
            type="email" 
            placeholder="請輸入 Email" 
            required
            :disabled="isLoading"
          >
        </div>

        <!-- 註冊按鈕 -->
        <button 
          type="submit" 
          class="submit-btn"
          :disabled="isLoading"
          :class="{ 'btn-loading': isLoading }"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? '註冊中...' : '立即註冊' }}
        </button>
      </form>

      <!-- 分隔線 -->
      <div class="divider">
        <span>或是</span>
      </div>

      <!-- 登入連結 -->
      <div class="register_area">
        <span>已經有帳號了？</span>
        <NuxtLink to="/login" class="link_highlight">立即登入</NuxtLink>
      </div>
    </div>
  </div>
</template>


<style src="@/assets/css/RegisterCard.css" scoped></style>
<style scoped>
.field-error {
  color: #E25E5E;
  font-size: 13px;
  margin-top: 6px;
  text-align: left;
  padding-left: 4px;
  animation: fadeIn 0.3s;
}

.has-error {
  border-color: #E25E5E !important;
  box-shadow: 0 0 0 2px rgba(226, 94, 94, 0.1) !important;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-3px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>