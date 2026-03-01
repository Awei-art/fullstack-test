<script setup>
import { ref } from 'vue';

definePageMeta({
  layout: 'default',
  middleware: 'auth'
});

const config = useRuntimeConfig();
const userCookie = useCookie('user_info');

const formData = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
});

const isSaving = ref(false);
const saveMessage = ref('');
const errorMessage = ref('');

const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;

const updatePassword = async () => {
  if (isSaving.value) return;

  errorMessage.value = '';
  saveMessage.value = '';

  if (!formData.value.old_password) {
    errorMessage.value = '請輸入目前的密碼。';
    return;
  }
  
  if (!formData.value.new_password) {
    errorMessage.value = '請輸入新密碼。';
    return;
  }

  if (formData.value.new_password !== formData.value.confirm_password) {
    errorMessage.value = '兩次輸入的新密碼不一致，請重新確認。';
    return;
  }

  const token = userCookie.value?.token;
  if (!token) {
    navigateTo('/login');
    return;
  }

  isSaving.value = true;

  try {
    const response = await $fetch('/auth/password/change/', {
      baseURL: getApiBase(),
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: {
        old_password: formData.value.old_password,
        new_password: formData.value.new_password
      }
    });

    saveMessage.value = response.message || '密碼已成功更新！';
    
    // 清空表單
    formData.value.old_password = '';
    formData.value.new_password = '';
    formData.value.confirm_password = '';
    
    // 3秒後清除成功訊息
    setTimeout(() => {
      saveMessage.value = '';
    }, 3000);
    
  } catch (err) {
    errorMessage.value = err.data?.error || '密碼更新失敗，請檢查您的輸入。';
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <div class="member-page-container">
    <div class="content-wrapper">
      <MemberSidebar />

      <main class="dashboard-content">
        <div class="member-banner">
          <div class="banner-info">
            <h1 class="welcome-text">修改登入密碼</h1>
            <p class="join-date">定期更新密碼，保護您的帳號安全。</p>
          </div>
        </div>

        <div v-if="saveMessage" class="global-success-msg">
            <svg xmlns="http://www.w3.org/2000/svg" class="success-icon" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            {{ saveMessage }}
        </div>

        <div class="info-grid">
          <div class="info-card" style="grid-column: 1 / -1; max-width: 500px;">
            <div class="card-header">
              <h3>變更密碼</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="updatePassword" class="profile-form">
                
                <div class="form-group">
                  <label class="form-label">目前的密碼 <span class="required-star">*</span></label>
                  <input 
                    v-model="formData.old_password" 
                    type="password" 
                    class="form-input" 
                    placeholder="請輸入您現在正在使用的密碼" 
                    :disabled="isSaving"
                    required
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">新密碼 <span class="required-star">*</span></label>
                  <input 
                    v-model="formData.new_password" 
                    type="password" 
                    class="form-input" 
                    placeholder="請輸入新密碼 (8碼以上，需包含大小寫英文及數字)" 
                    :disabled="isSaving"
                    required
                  />
                  <span class="password-hint">密碼強度要求：至少 8 個字元，且必須包含英文大寫、小寫字母與阿拉伯數字。</span>
                </div>

                <div class="form-group">
                  <label class="form-label">確認新密碼 <span class="required-star">*</span></label>
                  <input 
                    v-model="formData.confirm_password" 
                    type="password" 
                    class="form-input" 
                    placeholder="請再次輸入新密碼" 
                    :disabled="isSaving"
                    required
                  />
                </div>

                <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>

                <div class="form-actions">
                  <button type="submit" class="submit-btn" :disabled="isSaving">
                    <span v-if="isSaving" class="spinner-small"></span>
                    {{ isSaving ? '更新中...' : '確認更新密碼' }}
                  </button>
                </div>
                
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style src="@/assets/css/Member_page.css" scoped></style>
<style scoped>
/* 共用 Form 樣式 */
.profile-form { display: flex; flex-direction: column; gap: 24px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-label { font-size: 15px; font-weight: 600; color: #444; }
.required-star { color: #E25E5E; }
.form-input { padding: 14px 16px; border: 1px solid #dcdcdc; border-radius: 8px; font-size: 15px; color: #333; transition: all 0.2s; background-color: #fcfcfc; width: 100%; box-sizing: border-box; }
.form-input:focus { border-color: #C1A96C; outline: none; background-color: #ffffff; box-shadow: 0 0 0 3px rgba(193, 169, 108, 0.15); }
.form-input:disabled { background-color: #f0f0f0; cursor: not-allowed; opacity: 0.7; }

.password-hint { font-size: 13px; color: #888; margin-top: 4px; line-height: 1.4; }

.form-actions { margin-top: 10px; border-top: 1px solid #eee; padding-top: 24px; }
.submit-btn { width: 100%; background-color: #C1A96C; color: white; border: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; }
.submit-btn:hover:not(:disabled) { background-color: #b0985c; transform: translateY(-1px); }
.submit-btn:disabled { background-color: #d3d3d3; cursor: not-allowed; transform: none; }

.error-msg { color: #E25E5E; font-size: 14px; background-color: #FEE2E2; padding: 12px 16px; border-radius: 8px; border: 1px solid #fecaca; display: flex; align-items: center; gap: 8px; }
.global-success-msg { background-color: #E8F5E9; color: #2F8A3B; padding: 12px 20px; border-radius: 8px; font-weight: 500; margin-bottom: 24px; display: flex; align-items: center; gap: 8px; border: 1px solid #c8e6c9; }
.success-icon { width: 20px; height: 20px; }

.spinner-small { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
