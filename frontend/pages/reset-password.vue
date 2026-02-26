<script setup>
import { ref, onMounted } from 'vue';

// 使用 auth 版型來移除 Header 與 Footer
definePageMeta({
  layout: 'auth'
});

const route = useRoute();
const config = useRuntimeConfig();

const uid = ref('');
const token = ref('');
const password = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);
const message = ref('');
const errorMessage = ref('');
const isSuccess = ref(false);

onMounted(() => {
  uid.value = route.query.uid || '';
  token.value = route.query.token || '';
});

const submitResetPassword = async () => {
  if (!uid.value || !token.value) {
    errorMessage.value = '無效的重設密碼連結。';
    return;
  }
  
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '兩次輸入的密碼不一致。';
    return;
  }
  
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  if (!passwordRegex.test(password.value)) {
    errorMessage.value = '密碼必須至少 8 碼，且包含大寫英文、小寫英文與數字。';
    return;
  }

  isLoading.value = true;
  message.value = '';
  errorMessage.value = '';
  
  try {
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    const response = await $fetch('/auth/reset-password/', {
      baseURL: baseURL,
      method: 'POST',
      body: { 
        uid: uid.value,
        token: token.value,
        password: password.value
      }
    });
    
    isSuccess.value = true;
    message.value = '密碼重設成功！您現在可以使用新密碼重新登入了。';
    
  } catch (err) {
    if (err.data && err.data.error) {
       errorMessage.value = err.data.error;
    } else {
       errorMessage.value = '重設失敗，這個重設連結可能已經過期。';
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
        <h2 class="title" v-if="!isSuccess">設定新密碼</h2>
        <h2 class="title" v-else>密碼修改成功</h2>
      </div>

      <form @submit.prevent="submitResetPassword" class="auth-form" v-if="!isSuccess">
        <div class="form-group">
          <input
            v-model="password"
            type="password"
            placeholder="請輸入新密碼 (8碼以上，須含大小寫英文與數字)"
            class="form-input"
            required
            :disabled="isLoading"
          />
        </div>

        <div class="form-group" style="margin-top:20px;">
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="請再次輸入新密碼"
            class="form-input"
            required
            :disabled="isLoading"
          />
        </div>

        <div v-if="errorMessage" class="error-alert" style="margin-top:20px;">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="submit-btn"
          style="margin-top:20px;"
          :disabled="isLoading || !password || !confirmPassword"
          :class="{ 'btn-loading': isLoading }"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? '修改中...' : '確認修改' }}
        </button>
      </form>

      <!-- 成功畫面 -->
      <div v-else class="success-box">
        <svg xmlns="http://www.w3.org/2000/svg" class="success-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <p class="success-text">{{ message }}</p>
        <div style="margin-top: 20px;">
          <NuxtLink to="/login" class="submit-btn" style="text-decoration:none; display:inline-block; padding:12px 24px; text-align:center;">馬上前往登入</NuxtLink>
        </div>
      </div>
      
      <div class="divider" v-if="!isSuccess"></div>
      
      <div class="register-section" v-if="!isSuccess">
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
  line-height: 1.6;
}
</style>
