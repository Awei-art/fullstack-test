<script setup>
import { ref, computed, onMounted } from 'vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const config = useRuntimeConfig()
const userCookie = useCookie('user_info')
const isLoading = ref(true)
const orders = ref([])
const expandedOrderId = ref(null)
const orderDetails = ref({})

// 蝦皮風格分頁
const activeTab = ref('all')
const tabs = [
  { key: 'all', label: '全部' },
  { key: 'pending_payment', label: '待付款' },
  { key: 'pending_shipment', label: '待出貨' },
  { key: 'shipped', label: '待收貨' },
  { key: 'completed', label: '已完成' },
  { key: 'cancelled', label: '已取消' },
]

// 狀態設定
const statusConfig = {
  pending_payment:  { label: '待付款', color: '#e74c3c', bg: '#fdedec', icon: 'fa-clock' },
  pending_shipment: { label: '待出貨', color: '#e67e22', bg: '#fef5e7', icon: 'fa-box' },
  shipped:          { label: '待收貨', color: '#2980b9', bg: '#ebf5fb', icon: 'fa-truck' },
  completed:        { label: '已完成', color: '#27ae60', bg: '#eafaf1', icon: 'fa-check-circle' },
  cancelled:        { label: '已取消', color: '#95a5a6', bg: '#f2f3f4', icon: 'fa-times-circle' },
}

// 根據選中分頁過濾訂單
const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orders.value
  return orders.value.filter(o => o.status === activeTab.value)
})

// 各分頁數量
const tabCounts = computed(() => {
  const counts = {}
  tabs.forEach(t => {
    if (t.key === 'all') {
      counts[t.key] = orders.value.length
    } else {
      counts[t.key] = orders.value.filter(o => o.status === t.key).length
    }
  })
  return counts
})

const formatPrice = (price) => {
  return 'NT$ ' + price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const h = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${y}/${m}/${day} ${h}:${min}`
}

onMounted(async () => {
  await fetchOrders()
})

async function fetchOrders() {
  isLoading.value = true
  try {
    const user = userCookie.value
    if (!user?.token) return

    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/orders/`, {
      headers: { Authorization: `Bearer ${user.token}` }
    })
    orders.value = res
  } catch (e) {
    console.error('載入訂單失敗:', e)
  } finally {
    isLoading.value = false
  }
}

async function toggleOrderDetail(order) {
  if (expandedOrderId.value === order.id) {
    expandedOrderId.value = null
    return
  }
  expandedOrderId.value = order.id

  if (!orderDetails.value[order.order_number]) {
    try {
      const user = userCookie.value
      const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
      const res = await $fetch(`${apiBase}/orders/${order.order_number}/`, {
        headers: { Authorization: `Bearer ${user.token}` }
      })
      orderDetails.value[order.order_number] = res
    } catch (e) {
      console.error('載入訂單明細失敗:', e)
    }
  }
}

function getDetail(orderNumber) {
  return orderDetails.value[orderNumber]
}

// 重新前往 ECPay 付款
const payingOrderNumber = ref(null)
async function goToPayment(order) {
  payingOrderNumber.value = order.order_number
  try {
    const user = userCookie.value
    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/payment/repay/${order.order_number}/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${user.token}` }
    })

    if (res.payment) {
      const form = document.createElement('form')
      form.method = 'POST'
      form.action = res.payment.payment_url
      form.style.display = 'none'

      for (const [key, value] of Object.entries(res.payment.params)) {
        const input = document.createElement('input')
        input.type = 'hidden'
        input.name = key
        input.value = value
        form.appendChild(input)
      }

      document.body.appendChild(form)
      form.submit()
    }
  } catch (e) {
    console.error('前往付款失敗:', e)
    alert('無法前往付款，請稍後再試')
  } finally {
    payingOrderNumber.value = null
  }
}
</script>

<template>
  <div class="member_page_layout">
    <MemberSidebar />

    <div class="member_content">
      <h2 class="page_title">訂單狀態</h2>

      <ClientOnly>
        <!-- 分頁 Tabs -->
        <div class="order_tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            class="tab_btn"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
            <span v-if="tabCounts[tab.key] > 0 && tab.key !== 'all'" class="tab_badge">
              {{ tabCounts[tab.key] }}
            </span>
          </button>
        </div>

        <!-- 載入中 -->
        <div v-if="isLoading" class="loading_box">
          <div class="spinner"></div>
          <p>載入訂單中...</p>
        </div>

        <!-- 沒有訂單 -->
        <div v-else-if="filteredOrders.length === 0" class="empty_orders">
          <i class="fas fa-receipt"></i>
          <p v-if="activeTab === 'all'">目前還沒有任何訂單</p>
          <p v-else>沒有{{ tabs.find(t => t.key === activeTab)?.label }}的訂單</p>
          <NuxtLink to="/" class="shop_btn" v-if="activeTab === 'all'">前往選購</NuxtLink>
        </div>

        <!-- 訂單列表 -->
        <div v-else class="orders_list">
          <div
            v-for="order in filteredOrders"
            :key="order.id"
            class="order_card"
            :class="{ expanded: expandedOrderId === order.id }"
          >
            <!-- 訂單卡片頂部狀態條 -->
            <div class="order_status_bar">
              <span class="order_date">{{ formatDate(order.created_at) }}</span>
              <span
                class="status_badge"
                :style="{ color: statusConfig[order.status]?.color || '#666', background: statusConfig[order.status]?.bg || '#f0f0f0' }"
              >
                <i class="fas" :class="statusConfig[order.status]?.icon || 'fa-circle'"></i>
                {{ statusConfig[order.status]?.label || order.status_display || order.status }}
              </span>
            </div>

            <!-- 訂單主要資訊 -->
            <div class="order_card_body" @click="toggleOrderDetail(order)">
              <div class="order_item_preview">
                <img
                  v-if="order.first_item_image"
                  :src="order.first_item_image"
                  class="preview_img"
                  @error="$event.target.style.display = 'none'"
                >
                <div class="preview_info">
                  <span class="order_number">{{ order.order_number }}</span>
                  <span class="order_meta">
                    {{ order.payment_method_display }} · {{ order.item_count }} 件商品
                  </span>
                </div>
              </div>
              <div class="order_right">
                <span class="order_total">{{ formatPrice(order.total_amount) }}</span>
                <i class="fas fa-chevron-down expand_icon" :class="{ rotated: expandedOrderId === order.id }"></i>
              </div>
            </div>

            <!-- 操作按鈕列 -->
            <div class="order_actions" v-if="order.status === 'pending_payment'">
              <span class="action_hint">請盡速完成付款</span>
              <button
                v-if="order.payment_method === 'credit_card'"
                class="pay_btn"
                :disabled="payingOrderNumber === order.order_number"
                @click.stop="goToPayment(order)"
              >
                <i class="fas" :class="payingOrderNumber === order.order_number ? 'fa-spinner fa-spin' : 'fa-credit-card'"></i>
                {{ payingOrderNumber === order.order_number ? '跳轉中...' : '前往付款' }}
              </button>
            </div>

            <!-- 展開詳情 -->
            <div v-if="expandedOrderId === order.id" class="order_detail_panel">
              <div v-if="!getDetail(order.order_number)" class="detail_loading">
                載入明細中...
              </div>
              <div v-else class="detail_content">
                <!-- 收件資訊 -->
                <div class="detail_section">
                  <h4><i class="fas fa-map-marker-alt"></i> 收件資訊</h4>
                  <p><strong>{{ getDetail(order.order_number).receiver_name }}</strong> / {{ getDetail(order.order_number).receiver_phone }}</p>
                  <p>{{ getDetail(order.order_number).shipping_city }}{{ getDetail(order.order_number).shipping_district }}{{ getDetail(order.order_number).shipping_address }}</p>
                </div>

                <!-- 商品明細 -->
                <div class="detail_section">
                  <h4><i class="fas fa-shopping-bag"></i> 商品明細</h4>
                  <div class="detail_items">
                    <div v-for="item in getDetail(order.order_number).items" :key="item.id" class="detail_item_row">
                      <img v-if="item.product_image" :src="item.product_image" class="detail_item_img" @error="$event.target.style.display='none'">
                      <div class="detail_item_info">
                        <span class="detail_item_name">{{ item.product_name }}</span>
                        <span v-if="item.grade_name" class="detail_item_sub">{{ item.grade_name }}</span>
                        <span v-if="item.variety_names" class="detail_item_sub">{{ item.variety_names }}</span>
                      </div>
                      <span class="detail_item_qty">x{{ item.quantity }}</span>
                      <span class="detail_item_price">{{ formatPrice(item.item_total) }}</span>
                    </div>
                  </div>
                </div>

                <!-- 金額 -->
                <div class="detail_section detail_totals">
                  <div class="detail_total_row">
                    <span>商品小計</span>
                    <span>{{ formatPrice(getDetail(order.order_number).subtotal) }}</span>
                  </div>
                  <div v-if="getDetail(order.order_number).discount_amount > 0" class="detail_total_row" style="color: #C5374E;">
                    <span>優惠折抵 <span v-if="getDetail(order.order_number).coupon_code" style="font-size: 0.8rem;">({{ getDetail(order.order_number).coupon_code }})</span></span>
                    <span>- {{ formatPrice(getDetail(order.order_number).discount_amount) }}</span>
                  </div>
                  <div class="detail_total_row">
                    <span>運費</span>
                    <span>{{ getDetail(order.order_number).shipping_fee === 0 ? '免運費' : formatPrice(getDetail(order.order_number).shipping_fee) }}</span>
                  </div>
                  <div class="detail_total_row final">
                    <span>訂單總額</span>
                    <span>{{ formatPrice(getDetail(order.order_number).total_amount) }}</span>
                  </div>
                </div>

                <!-- 備註 -->
                <div v-if="getDetail(order.order_number).note" class="detail_section">
                  <h4><i class="fas fa-sticky-note"></i> 備註</h4>
                  <p class="detail_note">{{ getDetail(order.order_number).note }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </ClientOnly>
    </div>
  </div>
</template>

<style scoped>
.member_page_layout {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  gap: 40px;
}

.member_content {
  flex: 1;
  min-width: 0;
}

.page_title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
  padding-bottom: 12px;
  border-bottom: 2px solid #222;
}

/* ===== Tabs ===== */
.order_tabs {
  display: flex;
  border-bottom: 2px solid #eee;
  margin-bottom: 20px;
  overflow-x: auto;
  /* 隱藏滾動條但保持滑動 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}
.order_tabs::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}

.tab_btn {
  position: relative;
  padding: 12px 20px;
  background: none;
  border: none;
  font-size: 0.9rem;
  color: #888;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
}

.tab_btn:hover {
  color: #555;
}

.tab_btn.active {
  color: #C1A96C;
  border-bottom-color: #C1A96C;
  font-weight: 600;
}

.tab_badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #e74c3c;
  color: #fff;
  font-size: 0.68rem;
  font-weight: 600;
  margin-left: 4px;
  vertical-align: top;
}

/* ===== 載入/空狀態 ===== */
.loading_box {
  text-align: center;
  padding: 60px 0;
  color: #999;
}

.spinner {
  width: 36px;
  height: 36px;
  margin: 0 auto 16px;
  border: 3px solid #eee;
  border-top: 3px solid #C1A96C;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty_orders {
  text-align: center;
  padding: 60px 20px;
}

.empty_orders i {
  font-size: 2.5rem;
  color: #ddd;
  margin-bottom: 12px;
}

.empty_orders p {
  color: #999;
  margin-bottom: 16px;
}

.shop_btn {
  display: inline-block;
  padding: 10px 28px;
  background: #333;
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.shop_btn:hover { background: #C1A96C; }

/* ===== 訂單卡片 ===== */
.orders_list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.order_card {
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
  transition: box-shadow 0.2s;
}

.order_card:hover {
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

.order_card.expanded {
  border-color: #C1A96C;
}

/* 狀態條 */
.order_status_bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
}

.order_date {
  font-size: 0.8rem;
  color: #aaa;
}

.status_badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status_badge i {
  font-size: 0.7rem;
}

/* 卡片內容 */
.order_card_body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.15s;
}

.order_card_body:hover {
  background: #fdfbf7;
}

.order_item_preview {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
  min-width: 0;
}

.preview_img {
  width: 56px;
  height: 56px;
  border-radius: 4px;
  object-fit: cover;
  background: #f5f5f5;
  flex-shrink: 0;
}

.preview_info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.order_number {
  font-weight: 600;
  font-size: 0.92rem;
  color: #333;
}

.order_meta {
  font-size: 0.8rem;
  color: #999;
}

.order_right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order_total {
  font-size: 1.05rem;
  font-weight: 700;
  color: #333;
}

.expand_icon {
  color: #ccc;
  font-size: 0.75rem;
  transition: transform 0.25s ease;
}

.expand_icon.rotated {
  transform: rotate(180deg);
}

/* 操作按鈕列 */
.order_actions {
  padding: 10px 20px;
  background: #fffbf5;
  border-top: 1px solid #f5efe0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.action_hint {
  font-size: 0.82rem;
  color: #e74c3c;
  font-weight: 500;
}

.pay_btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 18px;
  background: #C1A96C;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.pay_btn:hover {
  background: #a8924e;
}

.pay_btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* ===== 展開面板 ===== */
.order_detail_panel {
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
  padding: 20px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.detail_loading {
  text-align: center;
  padding: 20px;
  color: #999;
}

.detail_section {
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid #eee;
}

.detail_section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.detail_section h4 {
  font-size: 0.85rem;
  font-weight: 600;
  color: #555;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.detail_section h4 i {
  color: #C1A96C;
  font-size: 0.82rem;
}

.detail_section p {
  margin: 2px 0;
  font-size: 0.85rem;
  color: #666;
  line-height: 1.6;
}

.detail_items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail_item_row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 0;
}

.detail_item_img {
  width: 42px;
  height: 42px;
  border-radius: 4px;
  object-fit: cover;
  background: #f0f0f0;
  flex-shrink: 0;
}

.detail_item_info {
  flex: 1;
  min-width: 0;
}

.detail_item_name {
  display: block;
  font-size: 0.85rem;
  color: #333;
  font-weight: 500;
}

.detail_item_sub {
  display: block;
  font-size: 0.73rem;
  color: #999;
}

.detail_item_qty {
  font-size: 0.82rem;
  color: #888;
  min-width: 28px;
  text-align: center;
}

.detail_item_price {
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
  min-width: 75px;
  text-align: right;
}

.detail_totals {
  background: #fff;
  border-radius: 4px;
  padding: 12px 14px !important;
}

.detail_total_row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.85rem;
  color: #666;
}

.detail_total_row.final {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 2px solid #333;
  margin-bottom: 0;
  font-weight: 700;
  color: #333;
  font-size: 0.95rem;
}

.detail_total_row.final span:last-child {
  color: #C5374E;
}

.detail_note {
  background: #f5f5f5;
  padding: 10px 12px;
  border-radius: 4px;
  font-size: 0.82rem;
  color: #666;
  white-space: pre-line;
}

/* RWD */
@media (max-width: 768px) {
  .member_page_layout {
    flex-direction: column;
    gap: 20px;
  }

  .order_tabs {
    gap: 0;
  }

  .tab_btn {
    padding: 10px 12px;
    font-size: 0.82rem;
  }

  .order_card_body {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .order_right {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
