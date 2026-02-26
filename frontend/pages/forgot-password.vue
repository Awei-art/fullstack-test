<script setup>
import { ref } from 'vue';

// 使用 auth 版型來移除 Header 與 Footer
definePageMeta({
  layout: 'auth'
});

const config = useRuntimeConfig();
const email = ref('');
const isLoading = ref(false);
const message = ref('');
const errorMessage = ref('');

const submitForgotPassword = async () => {
  if (!email.value) return;
  
  isLoading.value = true;
  message.value = '';
  errorMessage.value = '';
  
  try {
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    const response = await $fetch('/auth/forgot-password/', {
      baseURL: baseURL,
      method: 'POST',
      body: { email: email.value }
    });
    
    // 不論信箱對錯，為了資安我們統一發送成功訊息
    message.value = '如果該信箱已註冊，我們已經寄送了一封密碼重設信件。請檢查您的信箱。';
    
  } catch (err) {
    if (err.data && err.data.error) {
       errorMessage.value = err.data.error;
    } else {
       errorMessage.value = '系統發生未知的錯誤，請稍後再試。';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="card-header">
        <h2 class="title">忘記密碼</h2>
        <p class="subtitle">請輸入您當初註冊的 Email，我們會寄送一封重設密碼的連結給您。</p>
      </div>

      <form @submit.prevent="submitForgotPassword" class="auth-form" v-if="!message">
        <div class="form-group">
          <input
            v-model="email"
            type="email"
            placeholder="請輸入註冊的 Email 信箱"
            class="form-input"
            required
            :disabled="isLoading"
          />
        </div>

        <div v-if="errorMessage" class="error-alert">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="submit-btn"
          style="margin-top: 25px;"
          :disabled="isLoading || !email"
          :class="{ 'btn-loading': isLoading }"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? '發送中...' : '發送重設信件' }}
        </button>
      </form>

      <!-- 成功畫面 -->
      <div v-else class="success-box">
        <svg xmlns="http://www.w3.org/2000/svg" class="success-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="success-text">{{ message }}</p>
        <p class="success-tip">請不要忘記檢查您的垃圾郵件匣唷！</p>
      </div>

      <div class="divider"></div>

      <div class="register-section">
        <NuxtLink to="/login" class="register-link">返回登入畫面</NuxtLink>
      </div>
    </div>
  </div>
</template>

<style src="@/assets/css/LoginCard.css" scoped></style>
<style scoped>
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}
.auth-card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 40px 32px;
  width: 100%;
  max-width: 400px;
}
.subtitle {
  color: #666;
  font-size: 14px;
  margin-top: 10px;
  line-height: 1.5;
}
.success-box {
  text-align: center;
  padding: 20px 0;
}
.success-icon {
  width: 64px;
  height: 64px;
  color: #4CAF50;
  margin-bottom: 20px;
}
.success-text {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.6;
}
.success-tip {
  font-size: 13px;
  color: #888;
}
</style>
