<script setup>
import { ref, onMounted } from 'vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const config = useRuntimeConfig()
const userCookie = useCookie('user_info')

const isLoading = ref(true)
const coupons = ref([])

// 領取優惠券
const claimCode = ref('')
const isClaiming = ref(false)
const claimMessage = ref({ text: '', type: '' })

onMounted(async () => {
  await fetchCoupons()
})

async function fetchCoupons() {
  isLoading.value = true
  try {
    const user = userCookie.value
    if (!user?.token) return

    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/coupons/my/`, {
      headers: { Authorization: `Bearer ${user.token}` }
    })
    coupons.value = res
  } catch (e) {
    console.error('載入優惠券失敗:', e)
  } finally {
    isLoading.value = false
  }
}

async function handleClaim() {
  const code = claimCode.value.trim()
  if (!code) return
  
  isClaiming.value = true
  claimMessage.value = { text: '', type: '' }
  
  try {
    const user = userCookie.value
    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    
    const res = await $fetch(`${apiBase}/coupons/claim/`, {
      method: 'POST',
      headers: { 
        Authorization: `Bearer ${user.token}`,
        'Content-Type': 'application/json'
      },
      body: { coupon_code: code }
    })
    
    claimMessage.value = { text: res.message, type: 'success' }
    claimCode.value = ''
    
    // 重新載入列表
    await fetchCoupons()
    
  } catch (e) {
    claimMessage.value = { text: e.data?.error || '領取失敗', type: 'error' }
  } finally {
    isClaiming.value = false
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}/${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`
}

const getDiscountText = (couponData) => {
  if (couponData.discount_type === 'percent') {
    let v = parseFloat(couponData.discount_value);
    // 台灣折數習慣：90 -> 9折，85 -> 85折
    if (v % 10 === 0) {
      v = v / 10;
    }
    return `${v} 折`
  } else if (couponData.discount_type === 'fixed') {
    return `折 NT$ ${Number(couponData.discount_value).toLocaleString()}`
  } else if (couponData.discount_type === 'free_shipping') {
    return '免運費'
  }
  return ''
}
</script>

<template>
  <div class="member_page_layout">
    <MemberSidebar />

    <div class="member_content">
      <h2 class="page_title">我的優惠券</h2>

      <div class="claim_section">
        <div class="claim_input_group">
          <input 
            type="text" 
            v-model="claimCode" 
            placeholder="請輸入優惠代碼" 
            class="claim_input"
            @keyup.enter="handleClaim"
          >
          <button 
            @click="handleClaim" 
            class="claim_btn"
            :disabled="isClaiming || !claimCode.trim()"
          >
            {{ isClaiming ? '領取中...' : '兌換' }}
          </button>
        </div>
        <p v-if="claimMessage.text" :class="['claim_msg', claimMessage.type]">
          {{ claimMessage.text }}
        </p>
      </div>

      <div v-if="isLoading" class="loading_box">
        <div class="spinner"></div>
        <p>載入中...</p>
      </div>

      <div v-else-if="coupons.length === 0" class="empty_box">
        <i class="fa-solid fa-ticket empty_icon"></i>
        <p>您的錢包目前沒有優惠券</p>
      </div>

      <div v-else class="coupon_list">
        <!-- 優惠券卡片 -->
        <div 
          v-for="item in coupons" 
          :key="item.id" 
          class="coupon_card"
          :class="{ 'is_disabled': item.is_used || item.status_msg !== '可使用' }"
        >
          <div class="coupon_left">
            <div class="discount_offer">{{ getDiscountText(item.coupon) }}</div>
            <div class="min_spend" v-if="item.coupon.min_spend > 0">
              滿 NT$ {{ Number(item.coupon.min_spend).toLocaleString() }} 可用
            </div>
            <div class="min_spend" v-else>無低消門檻</div>
          </div>
          
          <div class="coupon_right">
            <div class="coupon_header">
              <h3 class="coupon_title">{{ item.coupon.title }}</h3>
              <span class="coupon_status" :class="item.status_msg === '可使用' ? 'status_valid' : 'status_invalid'">
                {{ item.status_msg }}
              </span>
            </div>
            
            <div class="coupon_code">代碼：{{ item.coupon.code }}</div>
            
            <div class="coupon_date">
              有效期限：{{ formatDate(item.coupon.valid_from) }} ~ {{ formatDate(item.coupon.valid_to) }}
            </div>
            
            <div v-if="item.is_used" class="used_at">
              使用時間：{{ formatDate(item.used_at) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.member_page_layout {
  display: flex;
  max-width: 1200px;
  margin: 40px auto;
  gap: 40px;
  padding: 0 20px;
}

.member_content {
  flex: 1;
  background-color: #fff;
}

.page_title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 24px;
  border-bottom: 2px solid #5A4098;
  padding-bottom: 10px;
  display: inline-block;
}

/* 領取區塊 */
.claim_section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 30px;
}

.claim_input_group {
  display: flex;
  gap: 12px;
  max-width: 500px;
}

.claim_input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  outline: none;
}

.claim_input:focus {
  border-color: #5A4098;
}

.claim_btn {
  background-color: #5A4098;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.claim_btn:hover:not(:disabled) {
  background-color: #4a3480;
}

.claim_btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.claim_msg {
  margin-top: 10px;
  font-size: 0.9rem;
}
.claim_msg.success { color: #27ae60; }
.claim_msg.error { color: #e74c3c; }

/* 優惠券列表 */
.coupon_list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

/* 優惠券卡片 */
.coupon_card {
  display: flex;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  background: white;
  transition: transform 0.2s;
}

.coupon_card.is_disabled {
  opacity: 0.6;
  filter: grayscale(100%);
}

.coupon_card:not(.is_disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(90, 64, 152, 0.1);
}

/* 左側票根造型 */
.coupon_left {
  background: linear-gradient(135deg, #5A4098, #7E65B8);
  color: white;
  padding: 20px;
  width: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
  border-right: 2px dashed rgba(255,255,255,0.5);
}

.is_disabled .coupon_left {
  background: #95a5a6;
}

.discount_offer {
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: 8px;
}

.min_spend {
  font-size: 0.8rem;
  opacity: 0.9;
}

/* 右側資訊 */
.coupon_right {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.coupon_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.coupon_title {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
}

.coupon_status {
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 12px;
  white-space: nowrap;
}

.status_valid {
  background-color: #eafaf1;
  color: #27ae60;
}

.status_invalid {
  background-color: #f2f3f4;
  color: #7f8c8d;
}

.coupon_code {
  font-size: 0.9rem;
  color: #666;
  background: #f9f9f9;
  padding: 6px 10px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 12px;
  border: 1px solid #ebebeb;
}

.coupon_date, .used_at {
  font-size: 0.8rem;
  color: #999;
}

.used_at {
  margin-top: 4px;
  color: #e74c3c;
}

/* 載入與空狀態 */
.loading_box, .empty_box {
  text-align: center;
  padding: 60px 0;
  color: #666;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #5A4098;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty_icon {
  font-size: 3rem;
  color: #ddd;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .member_page_layout {
    flex-direction: column;
  }
  .coupon_list {
    grid-template-columns: 1fr;
  }
}
</style>
