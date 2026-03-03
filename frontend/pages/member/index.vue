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
  joinDate: '',
  avatar: ''
});

// 帳號資料
const accountData = ref({
  email: '',
  phone: ''
});

// 最近登入紀錄
const recentLogins = ref([]);

// 最近的訂單資料
const recentOrder = ref(null);

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
    
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;
    
    // 同時抓取會員資料與訂單列表
    const [realData, ordersData] = await Promise.all([
      $fetch('/profile/', {
        baseURL: baseURL,
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      $fetch('/orders/', {
        baseURL: baseURL,
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      }).catch(err => {
        console.error('抓取訂單失敗', err);
        return [];
      })
    ]);

    if (realData) {
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
        name: realData.first_name || realData.username, // 優先使用顯示名稱
        level: realData.level || '一般會員',
        joinDate: formatDate(realData.date_joined),
        avatar: realData.avatar || '/images/default_avatar.png' // 設定預設頭貼
      };

      accountData.value = {
        email: realData.email,
        phone: realData.phone || '未設定'
      };

      recentLogins.value = (realData.recent_logins || []).map((record, index) => {
        // 第一筆當作「目前登入中」
        const isCurrent = index === 0;
        // 使用後端提供的所在地理位置
        const locationStr = record.location || '未知確切地點';
        return {
          time: formatDateTime(record.login_time),
          location: locationStr, 
          device: record.device_info || '未知裝置',
          isCurrent: isCurrent
        };
      });
      // 確保至少有一筆
      if (recentLogins.value.length === 0) {
        recentLogins.value.push({ time: formatDateTime(realData.last_login), location: '台灣 (預設)', device: '預設裝置' });
      }
      
      // 處理最新的訂單資料
      if (ordersData && ordersData.length > 0) {
        // 依據建立時間降冪排序 (最新的在前面)
        const sortedOrders = ordersData.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        const latest = sortedOrders[0];
        recentOrder.value = {
          order_number: latest.order_number,
          date: formatDate(latest.created_at),
          total: Number(latest.total_amount).toLocaleString(),
          status_display: latest.status_display
        };
      } else {
        recentOrder.value = null; // 尚無訂單
      }
    }

  } catch (err) {
    console.error('系統錯誤:', err);
    if (err.response?.status === 401 || err.data?.statusCode === 401) {
      userCookie.value = null;
      window.location.href = '/login';
    }
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
            <div class="banner-info" style="display: flex; align-items: center; gap: 20px;">
              <!-- 顯示大頭貼 -->
              <img :src="memberInfo.avatar" alt="Avatar" class="member-avatar" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
              <div>
                <div class="level-badge">{{ memberInfo.level }}</div>
                <h1 class="welcome-text">早安，{{ memberInfo.name }}</h1>
                <p class="join-date">加入日期：{{ memberInfo.joinDate }}</p>
              </div>
            </div>
          </div>

          <!-- Info Grid -->
          <div class="info-grid">
            
            <!-- Card A: Recent Order -->
            <div class="info-card">
              <div class="card-header">
                <h3>最近訂單</h3>
                <NuxtLink to="/member/orders" class="more-link">查看全部 ›</NuxtLink>
              </div>
              <div class="card-body" v-if="recentOrder">
                <div class="order-status-highlight">
                  {{ recentOrder.status_display }}
                </div>
                <div class="order-details">
                  <p>訂單編號：#{{ recentOrder.order_number }}</p>
                  <p>訂單日期：{{ recentOrder.date }}</p>
                  <p class="order-total">總金額：NT$ {{ recentOrder.total }}</p>
                </div>
              </div>
              <!-- 尚無訂單時的畫面 -->
              <div class="card-body" v-else style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 0;">
                <p style="color: #999; margin-bottom: 15px;">目前還沒有訂單紀錄</p>
                <NuxtLink to="/products" class="action-btn" style="text-decoration: none; text-align: center; display: inline-block;">去逛逛商品</NuxtLink>
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

            <!-- Card C: Last Logins -->
            <div class="info-card">
              <div class="card-header">
                <h3>最近登入紀錄</h3>
              </div>
              <div class="card-body">
                <div v-for="(login, index) in recentLogins" :key="index" style="margin-bottom: 12px; border-bottom: 1px dashed #eee; padding-bottom: 8px;">
                  <!-- 第一筆紀錄才會增加顯示綠燈狀態 -->
                  <div v-if="login.isCurrent" style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <div style="width: 8px; height: 8px; background-color: #4CAF50; border-radius: 50%; box-shadow: 0 0 4px #4CAF50;"></div>
                    <div style="font-size: 13px; color: #4CAF50; font-weight: bold;">目前登入中</div>
                  </div>
                  <!-- 無論哪一筆都統一顯示相同的紀錄格式 -->
                  <div style="display: flex; flex-direction: column;">
                    <div style="font-size: 13px; color: #555; font-weight: bold;">{{ login.location }}</div>
                    <div style="font-size: 12px; color: #999; margin-top: 2px;">{{ login.time }}</div>
                  </div>
                </div>
                <p class="security-tip" style="margin-top: 15px; font-size: 12px; color: #8bc34a;">若有未知的登入活動，請立即修改密碼。保護您的帳號安全。</p>
              </div>
            </div>

          </div>
        </template>
      </main>
    </div>
  </div>
</template>


<style src="@/assets/css/Member_page.css" scoped></style>
