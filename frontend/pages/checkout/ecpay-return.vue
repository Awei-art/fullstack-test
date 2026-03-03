<script setup>
import { ref, onMounted } from 'vue'

definePageMeta({
  layout: 'default',
})

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()
const userCookie = useCookie('user_info')

const isLoading = ref(true)
const paymentResult = ref(null)
const errorMsg = ref('')

onMounted(async () => {
  // ECPay 會透過 POST 回傳結果到 OrderResultURL
  // 但在前端我們用 query 參數來取得訂單編號
  // ECPay 的 OrderResultURL 會帶上 MerchantTradeNo 等參數
  
  // 從 URL 取得訂單編號（ECPay 回傳的參數或手動帶）
  const orderNumber = route.query.MerchantTradeNo || route.query.order || ''
  
  if (!orderNumber) {
    errorMsg.value = '無法取得訂單資訊'
    isLoading.value = false
    return
  }

  // 查詢後端付款狀態
  try {
    const user = userCookie.value
    if (!user?.token) {
      // 可能是未登入狀態（ECPay 跳回），引導到成功頁
      router.push({ path: '/checkout/success', query: { order: orderNumber } })
      return
    }

    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/payment/return/${orderNumber}/`, {
      headers: { Authorization: `Bearer ${user.token}` }
    })
    paymentResult.value = res

    // 等 2 秒後自動跳轉成功頁
    setTimeout(() => {
      router.push({ path: '/checkout/success', query: { order: orderNumber } })
    }, 2000)

  } catch (e) {
    console.error('查詢付款狀態失敗:', e)
    // 即使查詢失敗也跳到成功頁
    setTimeout(() => {
      router.push({ path: '/checkout/success', query: { order: orderNumber } })
    }, 2000)
  } finally {
    isLoading.value = false
  }
})

const formatPrice = (price) => {
  return 'NT$ ' + price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}
</script>

<template>
  <div class="ecpay_return_page">
    <ClientOnly>
      <div v-if="isLoading" class="return_content">
        <div class="spinner"></div>
        <p>正在確認付款結果...</p>
      </div>

      <div v-else-if="paymentResult" class="return_content">
        <div class="result_icon" :class="paymentResult.payment_status === 'paid' ? 'success' : 'pending'">
          <i class="fas" :class="paymentResult.payment_status === 'paid' ? 'fa-check' : 'fa-clock'"></i>
        </div>
        <h2 v-if="paymentResult.payment_status === 'paid'">付款成功！</h2>
        <h2 v-else>付款處理中</h2>
        <p>訂單編號：{{ paymentResult.order_number }}</p>
        <p v-if="paymentResult.payment_status === 'paid'" class="paid_hint">
          {{ formatPrice(paymentResult.total_amount) }} 已完成付款
        </p>
        <p class="redirect_hint">正在為您跳轉...</p>
      </div>

      <div v-else class="return_content">
        <div class="result_icon pending">
          <i class="fas fa-clock"></i>
        </div>
        <h2>處理中</h2>
        <p>{{ errorMsg || '正在確認付款結果，即將跳轉...' }}</p>
        <p class="redirect_hint">正在為您跳轉...</p>
      </div>
    </ClientOnly>
  </div>
</template>

<style scoped>
.ecpay_return_page {
  max-width: 500px;
  margin: 0 auto;
  padding: 80px 20px;
  text-align: center;
  font-family: 'Times New Roman', 'Noto Sans TC', sans-serif;
}

.return_content h2 {
  font-size: 1.5rem;
  margin: 16px 0 8px;
  color: #333;
}

.return_content p {
  color: #888;
  font-size: 0.95rem;
  margin: 4px 0;
}

.paid_hint {
  color: #27ae60 !important;
  font-weight: 600;
  font-size: 1.1rem !important;
  margin-top: 8px !important;
}

.redirect_hint {
  margin-top: 20px !important;
  font-size: 0.85rem !important;
  color: #bbb !important;
}

.result_icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  font-size: 1.8rem;
  animation: scaleUp 0.4s ease;
}

.result_icon.success {
  background: #27ae60;
  color: #fff;
}

.result_icon.pending {
  background: #e67e22;
  color: #fff;
}

@keyframes scaleUp {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 20px;
  border: 3px solid #eee;
  border-top: 3px solid #C1A96C;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
