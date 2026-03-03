<script setup>
import { onMounted, ref, nextTick } from 'vue'

const route = useRoute()
const config = useRuntimeConfig()
const isLoading = ref(true)
const errorMessage = ref('')

definePageMeta({
  layout: 'auth'
})

onMounted(async () => {
  // Google 授權後會把 code 帶在網址上
  const code = route.query.code

  if (!code) {
    errorMessage.value = '登入失敗，缺少授權碼'
    isLoading.value = false
    return
  }

  try {
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase

    // 將 code 送去後端，由後端向 Google 交換 token 和個人資料
    const response = await $fetch('/auth/google/', {
      baseURL: baseURL,
      method: 'POST',
      body: {
        code: code
      }
    })

    if (response) {
      // 登入成功，儲存 JWT token
      const userCookie = useCookie('user_info', {
        maxAge: 60 * 60 * 24 * 7 // 預設記住7天
      })
      
      userCookie.value = {
        token: response.access,
        refresh: response.refresh,
        username: response.name || response.username,
        avatar: response.avatar || ''
      }

      // 等待 Cookie 確實寫入後再跳轉
      await nextTick()
      await new Promise(resolve => setTimeout(resolve, 100))
      await navigateTo('/member', { replace: true })
    }

  } catch (err) {
    console.error('系統錯誤:', err)
    // $fetch 的錯誤訊息通常在 err.data
    errorMessage.value = err.data?.error || 'Google 登入處理失敗，請稍後再試'
    isLoading.value = false
  }
})
</script>

<template>
  <div class="callback-container">
    <div v-if="isLoading" class="loading-box">
      <span class="loading-spinner"></span>
      <p>Google 登入處理中，請稍候...</p>
    </div>
    
    <div v-else class="error-box">
      <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <p>{{ errorMessage }}</p>
      <NuxtLink to="/login" class="back-btn">返回登入頁</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.callback-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-family: 'Noto Sans TC', sans-serif;
}

.loading-box, .error-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4285F4; /* Google 藍色 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  width: 48px;
  height: 48px;
  color: #e74c3c;
}

.back-btn {
  margin-top: 10px;
  padding: 10px 24px;
  background-color: #333;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: background-color 0.2s;
}

.back-btn:hover {
  background-color: #555;
}
</style>
