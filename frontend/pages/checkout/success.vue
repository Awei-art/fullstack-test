<script setup>
import { ref, onMounted } from 'vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const config = useRuntimeConfig()
const route = useRoute()
const userCookie = useCookie('user_info')

const orderNumber = ref(route.query.order || '')
const orderData = ref(null)
const isLoading = ref(true)

const formatPrice = (price) => {
  return 'NT$ ' + price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

onMounted(async () => {
  if (!orderNumber.value) {
    isLoading.value = false
    return
  }

  try {
    const user = userCookie.value
    if (!user?.token) return

    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/orders/${orderNumber.value}/`, {
      headers: { Authorization: `Bearer ${user.token}` }
    })
    orderData.value = res
  } catch (e) {
    console.error('載入訂單失敗:', e)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="success_page">
    <ClientOnly>
      <!-- 載入中 -->
      <div v-if="isLoading" class="loading_state">
        <p>載入訂單資訊中...</p>
      </div>

      <!-- 成功畫面 -->
      <div v-else-if="orderData" class="success_content">
        <!-- 打勾動畫 -->
        <div class="success_icon">
          <div class="check_circle">
            <i class="fas fa-check"></i>
          </div>
        </div>

        <h1 class="success_title">訂單已成立！</h1>
        <p class="success_subtitle">感謝您的訂購，我們會盡快為您處理出貨。</p>

        <!-- 訂單編號 -->
        <div class="order_number_box">
          <span class="order_label">訂單編號</span>
          <span class="order_number">{{ orderData.order_number }}</span>
        </div>

        <!-- 訂單摘要 -->
        <div class="order_summary_card">
          <div class="summary_section">
            <h3>收件資訊</h3>
            <p><strong>{{ orderData.receiver_name }}</strong> / {{ orderData.receiver_phone }}</p>
            <p>{{ orderData.shipping_city }}{{ orderData.shipping_district }}{{ orderData.shipping_address }}</p>
          </div>

          <div class="summary_divider"></div>

          <div class="summary_section">
            <h3>付款方式</h3>
            <p>{{ orderData.payment_method_display }}</p>
            <div v-if="orderData.payment_method === 'transfer'" class="transfer_notice">
              <i class="fas fa-info-circle"></i>
              請於 3 個工作天內完成匯款，逾期訂單將自動取消。
            </div>
          </div>

          <div class="summary_divider"></div>

          <div class="summary_section">
            <h3>訂單明細</h3>
            <div v-for="item in orderData.items" :key="item.id" class="order_item_row">
              <div class="order_item_info">
                <span class="item_name">{{ item.product_name }}</span>
                <span v-if="item.grade_name" class="item_detail">{{ item.grade_name }}</span>
                <span v-if="item.variety_names" class="item_detail">{{ item.variety_names }}</span>
              </div>
              <div class="order_item_qty">x{{ item.quantity }}</div>
              <div class="order_item_price">{{ formatPrice(item.item_total) }}</div>
            </div>
          </div>

          <div class="summary_divider"></div>

          <div class="summary_section totals">
            <div class="total_row">
              <span>商品小計</span>
              <span>{{ formatPrice(orderData.subtotal) }}</span>
            </div>
            <div v-if="orderData.discount_amount > 0" class="total_row" style="color: #C5374E;">
              <span>優惠折抵 <span v-if="orderData.coupon_code" style="font-size: 0.8rem;">({{ orderData.coupon_code }})</span></span>
              <span>- {{ formatPrice(orderData.discount_amount) }}</span>
            </div>
            <div class="total_row">
              <span>運費</span>
              <span>{{ orderData.shipping_fee === 0 ? '免運費' : formatPrice(orderData.shipping_fee) }}</span>
            </div>
            <div class="total_row final">
              <span>應付總額</span>
              <span class="final_amount">{{ formatPrice(orderData.total_amount) }}</span>
            </div>
          </div>

          <div v-if="orderData.note" class="summary_section">
            <h3>備註</h3>
            <p class="note_text">{{ orderData.note }}</p>
          </div>
        </div>

        <!-- 按鈕 -->
        <div class="action_buttons">
          <NuxtLink to="/" class="action_btn primary">回到首頁</NuxtLink>
          <NuxtLink to="/member/orders" class="action_btn secondary">查看我的訂單</NuxtLink>
        </div>
      </div>

      <!-- 找不到訂單 -->
      <div v-else class="success_content">
        <div class="success_icon">
          <div class="check_circle warn">
            <i class="fas fa-exclamation"></i>
          </div>
        </div>
        <h1 class="success_title">找不到訂單資訊</h1>
        <p class="success_subtitle">您可能是直接訪問了這個頁面。</p>
        <div class="action_buttons">
          <NuxtLink to="/" class="action_btn primary">回到首頁</NuxtLink>
        </div>
      </div>
    </ClientOnly>
  </div>
</template>

<style scoped>
.success_page {
  max-width: 700px;
  margin: 0 auto;
  padding: 50px 20px 80px;
  font-family: 'Times New Roman', 'Noto Sans TC', sans-serif;
}

.loading_state {
  text-align: center;
  padding: 80px 0;
  color: #999;
}

.success_content {
  text-align: center;
}

/* 打勾動畫 */
.success_icon {
  margin-bottom: 24px;
}

.check_circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #27ae60;
  color: #fff;
  font-size: 2rem;
  animation: scaleUpBounce 0.5s ease forwards;
}

.check_circle.warn {
  background: #e67e22;
}

@keyframes scaleUpBounce {
  0% { transform: scale(0); opacity: 0; }
  60% { transform: scale(1.15); }
  100% { transform: scale(1); opacity: 1; }
}

.success_title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #222;
}

.success_subtitle {
  font-size: 1rem;
  color: #888;
  margin-bottom: 30px;
}

/* 訂單編號 */
.order_number_box {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 14px 28px;
  background: #fdfbf7;
  border: 1px dashed #C1A96C;
  border-radius: 6px;
  margin-bottom: 30px;
}

.order_label {
  font-size: 0.85rem;
  color: #888;
}

.order_number {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  letter-spacing: 1px;
}

/* 訂單摘要卡片 */
.order_summary_card {
  text-align: left;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 30px;
}

.summary_section {
  padding: 20px 24px;
}

.summary_section h3 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px 0;
  letter-spacing: 0.5px;
}

.summary_section p {
  margin: 4px 0;
  font-size: 0.9rem;
  color: #555;
  line-height: 1.6;
}

.summary_divider {
  border-top: 1px solid #f0f0f0;
}

.transfer_notice {
  margin-top: 8px;
  padding: 10px 14px;
  background: #fff8ed;
  border: 1px solid #f5d9a0;
  border-radius: 4px;
  font-size: 0.82rem;
  color: #b37700;
}

.transfer_notice i {
  margin-right: 6px;
}

/* 訂單商品列 */
.order_item_row {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f8f8f8;
  gap: 12px;
}

.order_item_row:last-child {
  border-bottom: none;
}

.order_item_info {
  flex: 1;
}

.item_name {
  display: block;
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
}

.item_detail {
  display: block;
  font-size: 0.78rem;
  color: #999;
}

.order_item_qty {
  font-size: 0.85rem;
  color: #888;
  min-width: 35px;
  text-align: center;
}

.order_item_price {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
  min-width: 80px;
  text-align: right;
}

/* 金額總計 */
.totals .total_row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #555;
}

.totals .total_row.final {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 2px solid #333;
  margin-bottom: 0;
}

.totals .total_row.final span:first-child {
  font-weight: 600;
  font-size: 1rem;
  color: #222;
}

.final_amount {
  font-size: 1.3rem !important;
  font-weight: 700 !important;
  color: #C5374E !important;
}

.note_text {
  background: #f9f9f9;
  padding: 10px 14px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #666;
}

/* 按鈕 */
.action_buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 10px;
}

.action_btn {
  padding: 12px 32px;
  border-radius: 4px;
  font-size: 0.95rem;
  font-family: inherit;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.action_btn.primary {
  background: #333;
  color: #fff;
  border: 1px solid #333;
}

.action_btn.primary:hover {
  background: #C1A96C;
  border-color: #C1A96C;
}

.action_btn.secondary {
  background: #fff;
  color: #333;
  border: 1px solid #ddd;
}

.action_btn.secondary:hover {
  border-color: #333;
}

@media (max-width: 768px) {
  .action_buttons {
    flex-direction: column;
    align-items: center;
  }

  .action_btn {
    width: 100%;
    max-width: 280px;
    text-align: center;
  }
}
</style>
