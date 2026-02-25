<script setup>
import { reactive, ref } from 'vue';

// 取得 API 設定
const config = useRuntimeConfig();

// 表單資料
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// 錯誤訊息
const errorMessage = ref('');

// 載入狀態
const isLoading = ref(false);

// 註冊處理函式
const handleRegister = async () => {
  // 防止重複點擊
  if (isLoading.value) return;

  // 清空錯誤訊息
  errorMessage.value = '';

  // 1. 前端驗證：檢查密碼是否一致
  if (form.password !== form.confirmPassword) {
    errorMessage.value = '兩次密碼輸入不一致';
    return;
  }

  // 2. 前端驗證：密碼長度
  if (form.password.length < 8) {
    errorMessage.value = '密碼至少需要 8 個字元';
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
        errorMessage.value = '註冊失敗，請稍後再試';
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
            type="text" 
            placeholder="請輸入帳號" 
            required
            :disabled="isLoading"
          >
        </div>

        <!-- 密碼 -->
        <div class="input_group">
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="設定密碼（至少 8 個字元）" 
            required
            minlength="8"
            :disabled="isLoading"
          >
        </div>

        <!-- 確認密碼 -->
        <div class="input_group">
          <input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="再次確認密碼" 
            required
            :disabled="isLoading"
          >
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