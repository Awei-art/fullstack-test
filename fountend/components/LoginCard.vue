<script setup>
import { reactive, ref } from 'vue';

// 取得 Nuxt 設定（API 網址）
const config = useRuntimeConfig();

// 表單資料
const form = reactive({
  account: '',
  password: '',
  rememberMe: false
});

// 錯誤訊息
const errorMessage = ref('');

// 載入狀態
const isLoading = ref(false);

// 登入處理函式
const handleLogin = async () => {
  // 防止重複點擊
  if (isLoading.value) return;

  // 開始載入
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // 🔥 修改：使用 config 的 API 網址，並改成 /token/ (JWT 登入端點)
    const { data, error } = await useFetch(`${config.public.apiBase}/token/`, {
      method: 'POST',
      body: {
        username: form.account,   // Django 預設用 username
        password: form.password
      }
    });

    // 處理錯誤
    if (error.value) {
      console.error('登入失敗:', error.value);
      
      // 根據錯誤狀態碼顯示不同訊息
      if (error.value.statusCode === 401) {
        errorMessage.value = '帳號或密碼錯誤，請重試。';
      } else if (error.value.statusCode === 400) {
        errorMessage.value = '請輸入完整的帳號和密碼。';
      } else {
        errorMessage.value = '登入失敗，請稍後再試。';
      }
      return;
    }

    // 登入成功
    if (data.value) {
      console.log('登入成功:', data.value);
      
      // 🔥 修改：儲存 Token 和使用者資訊到 Cookie
      const userCookie = useCookie('user_info', {
        maxAge: form.rememberMe ? 60 * 60 * 24 * 7 : undefined  // 記住我：7天，否則關閉瀏覽器就清除
      });
      
      userCookie.value = {
        token: data.value.access,        // JWT Access Token
        refresh: data.value.refresh,     // JWT Refresh Token (可選)
        username: form.account           // 儲存使用者名稱
      };

      // 跳轉到會員頁面
      await navigateTo('/member');
    }

  } catch (err) {
    console.error('連線錯誤:', err);
    errorMessage.value = '系統連線錯誤，請檢查網路後再試。';
  } finally {
    // 解除載入狀態
    isLoading.value = false;
  }
};
</script>


<template>
  <div class="login-wrapper">
    <div class="login-card">
      <!-- 卡片標題 -->
      <div class="card-header">
        <img src="/images/logo_icon.svg" alt="Logo" class="logo" />
        <h2 class="title">會員登入</h2>
      </div>

      <!-- 登入表單 -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- 帳號輸入 -->
        <div class="form-group">
          <input
            v-model="form.account"
            type="text"
            placeholder="請輸入帳號"
            class="form-input"
            required
            :disabled="isLoading"
          />
        </div>

        <!-- 密碼輸入 -->
        <div class="form-group">
          <input
            v-model="form.password"
            type="password"
            placeholder="請輸入密碼"
            class="form-input"
            required
            :disabled="isLoading"
          />
        </div>

        <!-- 記住我 & 忘記密碼 -->
        <div class="form-actions">
          <label class="remember-me">
            <input 
              type="checkbox" 
              v-model="form.rememberMe"
              :disabled="isLoading"
            />
            <span>記住帳號</span>
          </label>
          <NuxtLink to="/forgot-password" class="forgot-password">
            忘記密碼？
          </NuxtLink>
        </div>

        <!-- 🔥 新增：錯誤訊息提示 -->
        <div v-if="errorMessage" class="error-alert">
          <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          {{ errorMessage }}
        </div>

        <!-- 登入按鈕 -->
        <button 
          type="submit" 
          class="submit-btn"
          :disabled="isLoading"
          :class="{ 'btn-loading': isLoading }"
        >
          <!-- 🔥 修改：顯示載入動畫 -->
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? '登入中...' : '立即登入' }}
        </button>
      </form>

      <!-- 分隔線 -->
      <div class="divider">
        <span>或是</span>
      </div>

      <!-- 註冊連結 -->
      <div class="register-section">
        <span class="text">還不是會員？</span>
        <NuxtLink to="/register" class="register-link">立即註冊</NuxtLink>
      </div>
    </div>
  </div>
</template>

<style src="@/assets/css/LoginCard.css" scoped></style>


