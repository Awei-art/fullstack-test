// 定義使用者資訊的型別
interface UserInfo {
  token: string;
  // 其他可能的屬性
  username?: string;
  email?: string;
}

export default defineNuxtRouteMiddleware((to, from) => {
  // 1. 讀取 Cookie（登入時存的 Token）
  const userCookie = useCookie<UserInfo>('user_info');
  
  // 2. 檢查是否有 Token
  if (!userCookie.value?.token) {
    // 3. 沒有 Token → 跳轉到登入頁
    return navigateTo('/login');
  }
  
  // 4. 有 Token → 放行，繼續進入頁面
});