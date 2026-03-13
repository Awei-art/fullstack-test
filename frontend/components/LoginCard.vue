<script setup>
import { reactive, ref, computed, onMounted } from 'vue';

// 取得 Nuxt 設定（API 網址）
const config = useRuntimeConfig();

// LINE / Google 快速登入（動態偵測目前網址，不再寫死 localhost）
const lineLoginUrl = computed(() => {
  const origin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000';
  const redirectUri = encodeURIComponent(`${origin}/login/line-callback`);
  return `https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=2009217904&redirect_uri=${redirectUri}&state=login_state_123&scope=profile%20openid`;
});

const googleLoginUrl = computed(() => {
  const origin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000';
  const redirectUri = encodeURIComponent(`${origin}/login/google-callback`);
  return `https://accounts.google.com/o/oauth2/v2/auth?client_id=***REMOVED_GOOGLE_CLIENT_ID***&redirect_uri=${redirectUri}&response_type=code&scope=email%20profile&access_type=online`;
});

// 路由控制 (返回首頁)
const router = useRouter();
const goBack = () => {
  router.push('/');
};

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

// 頁面載入時讀取已記憶的帳號
onMounted(() => {
  const savedAccount = localStorage.getItem('saved_account');
  if (savedAccount) {
    form.account = savedAccount;
    form.rememberMe = true;
  }
});

// 登入處理函式
const handleLogin = async () => {
  // 防止重複點擊
  if (isLoading.value) return;

  // 開始載入
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // 使用 config 的 API 網址，並改成 /token/ (JWT 登入端點)
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    const { data, error } = await useFetch('/token/', {
      baseURL: baseURL,
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
      
      // 處理「記住帳號」 (localStorage)
      if (form.rememberMe) {
        localStorage.setItem('saved_account', form.account);
      } else {
        localStorage.removeItem('saved_account');
      }
      
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
      <!-- 返回按鈕 -->
      <button @click="goBack" class="back-btn">
        <svg xmlns="http://www.w3.org/2000/svg" class="back-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        返回
      </button>

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
            placeholder="請輸入帳號或 Email"
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

      <!-- 🔥 新增：LINE 登入按鈕 -->
      <a :href="lineLoginUrl" class="line-login-btn">
        <i class="fab fa-line line-icon"></i>
        <span>使用 LINE 快速登入</span>
      </a>

      <!-- 🔥 新增：Google 登入按鈕 -->
      <a :href="googleLoginUrl" class="google-login-btn">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="24px" height="24px" class="google-icon">
          <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
          <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
          <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
          <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
        </svg>
        <span>使用 Google 快速登入</span>
      </a>

      <!-- 註冊連結 -->
      <div class="register-section">
        <span class="text">還不是會員？</span>
        <NuxtLink to="/register" class="register-link">立即註冊</NuxtLink>
      </div>
    </div>
  </div>
</template>

<style src="@/assets/css/LoginCard.css" scoped></style>

<style scoped>
/* LINE 登入按鈕樣式 */
.line-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #06C755;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  padding: 12px 0;
  margin-bottom: 25px;
  font-weight: 500;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.line-login-btn:hover {
  background-color: #05b34c;
}

.line-icon {
  font-size: 1.5rem;
  margin-right: 10px;
}

/* Google 登入按鈕樣式 */
.google-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  color: #3c4043;
  text-decoration: none;
  border-radius: 8px;
  border: 1px solid #dadce0;
  padding: 12px 0;
  margin-bottom: 25px;
  font-weight: 500;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.google-login-btn:hover {
  background-color: #f8f9fa;
}

.google-icon {
  margin-right: 10px;
}
</style>
