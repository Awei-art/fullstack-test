<script setup>
import { ref, onMounted } from 'vue';

// 取得 Nuxt 設定
const config = useRuntimeConfig();

// 🔥 路由守衛
definePageMeta({
  layout: 'default',
  middleware: 'auth'
});

// 🔥 載入狀態（重要！）
const isLoading = ref(true);

// 會員基本資訊
const memberInfo = ref({
  name: '',
  level: '',
  joinDate: ''
});

// 帳號資料
const accountData = ref({
  email: '',
  phone: ''
});

// 最後登入
const lastLogin = ref({
  time: '',
  location: ''
});

// 訂單資料（假資料）
const recentOrder = ref({
  id: '#ABCD-123456',
  date: '2025-01-20',
  total: 'NT$ 1,280',
  status: '配送中'
});

// 🔥 Cookie
const userCookie = useCookie('user_info');

// 🔥 抓取會員資料
const fetchMemberData = async () => {
  const token = userCookie.value?.token;
  
  if (!token) {
    return navigateTo('/login');
  }

  try {
    isLoading.value = true; // 🔥 開始載入
    
    const { data, error } = await useFetch(`${config.public.apiBase}/profile/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (error.value) {
      console.error('抓取資料失敗:', error.value);
      
      if (error.value.statusCode === 401) {
        userCookie.value = null;
        return navigateTo('/login');
      }
      
      throw new Error('載入失敗');
    }

    if (data.value) {
      const realData = data.value;
      console.log('拿到真實資料:', realData);

      // 🔥 格式化日期
      const formatDate = (dateString) => {
        if (!dateString) return '未知';
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-TW');
      };

      const formatDateTime = (dateString) => {
        if (!dateString) return '首次登入';
        const date = new Date(dateString);
        return date.toLocaleString('zh-TW');
      };

      // 更新資料
      memberInfo.value = {
        name: realData.username,
        level: realData.level || '一般會員',
        joinDate: formatDate(realData.date_joined)
      };

      accountData.value = {
        email: realData.email,
        phone: realData.phone || '未設定'
      };

      lastLogin.value = {
        time: formatDateTime(realData.last_login),
        location: '台灣 (Chrome Windows)'
      };
    }

  } catch (err) {
    console.error('系統錯誤:', err);
  } finally {
    isLoading.value = false; // 🔥 載入完成
  }
};

// 🔥 登出功能
const handleLogout = () => {
  if (confirm('確定要登出嗎？')) {
    userCookie.value = null;
    navigateTo('/login');
  }
};

// 頁面載入時執行
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
        
        <!-- 🔥 載入中畫面 -->
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>載入中...</p>
        </div>

        <!-- 🔥 載入完成後才顯示 -->
        <template v-else>
          <!-- Top Banner -->
          <div class="member-banner">
            <div class="banner-info">
              <div class="level-badge">{{ memberInfo.level }}</div>
              <h1 class="welcome-text">早安，{{ memberInfo.name }}</h1>
              <p class="join-date">加入日期：{{ memberInfo.joinDate }}</p>
            </div>
            <!-- 🔥 登出按鈕 -->
            <button @click="handleLogout" class="logout-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              登出
            </button>
          </div>

          <!-- Info Grid -->
          <div class="info-grid">
            
            <!-- Card A: Recent Order -->
            <div class="info-card">
              <div class="card-header">
                <h3>最近訂單</h3>
                <NuxtLink to="/member/orders" class="more-link">查看全部 ›</NuxtLink>
              </div>
              <div class="card-body">
                <div class="order-status-highlight">
                  {{ recentOrder.status }}
                </div>
                <div class="order-details">
                  <p>訂單編號：{{ recentOrder.id }}</p>
                  <p>訂單日期：{{ recentOrder.date }}</p>
                  <p class="order-total">總金額：{{ recentOrder.total }}</p>
                </div>
              </div>
            </div>

            <!-- Card B: Account Data -->
            <div class="info-card">
              <div class="card-header">
                <h3>帳號資料</h3>
              </div>
              <div class="card-body">
                <div class="info-row">
                  <span class="label">Email</span>
                  <span class="value">{{ accountData.email }}</span>
                </div>
                <div class="info-row">
                  <span class="label">手機</span>
                  <span class="value">{{ accountData.phone }}</span>
                </div>
                <button class="action-btn">更改密碼</button>
              </div>
            </div>

            <!-- Card C: Last Login -->
            <div class="info-card">
              <div class="card-header">
                <h3>最近登入</h3>
              </div>
              <div class="card-body">
                <div class="login-time">{{ lastLogin.time }}</div>
                <div class="login-location">{{ lastLogin.location }}</div>
                <p class="security-tip">若非本人登入，請立即修改密碼</p>
              </div>
            </div>

          </div>
        </template>
      </main>
    </div>
  </div>
</template>


<style src="@/assets/css/Member_page.css" scoped></style>
