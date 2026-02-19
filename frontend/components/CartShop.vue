<script setup>
import { ref, computed } from 'vue'

// 假資料：模擬購物車內容
const cartItems = ref([
  {
    id: 1,
    title: '乾薑',
    variant: '容量: 500g',
    price: 18000,
    quantity: 3,
    image: '/images/dry-ginger-500.jpg' // 預設假圖路徑，前端需自行準備或用 placeholder
  },
  {
    id: 2,
    title: '乾薑',
    variant: '容量: 120克',
    price: 4200,
    quantity: 3,
    image: '/images/dry-ginger-120.jpg'
  },
  {
    id: 3,
    title: '乾薑',
    variant: '容量: 2 袋套裝',
    price: 1150,
    quantity: 2,
    image: '/images/dry-ginger-set.jpg'
  }
])

// 格式化金額 (千分位)
const formatPrice = (price) => {
  return 'NT$ ' + price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

const subtotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const totalQuantity = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.quantity, 0)
})

const shippingFee = ref(0) // dynamic later? for now 0 as per image "¥0"

const totalAmount = computed(() => {
  return subtotal.value + shippingFee.value
})

// 增加數量
const increaseQty = (item) => {
  item.quantity++
}

// 減少數量
const decreaseQty = (item) => {
  if (item.quantity > 1) {
    item.quantity--
  }
}

// 移除商品
const removeItem = (id) => {
  cartItems.value = cartItems.value.filter(item => item.id !== id)
}

// 繼續購物 (範例功能)
const continueShopping = () => {
  // 可導向首頁或商品頁
  navigateTo('/products')
}

// 結帳 (範例功能)
const checkout = () => {
  alert(`準備結帳：${formatPrice(subtotal.value)}`)
}
</script>

<template>
  <div class="cart_page">
    <h1 class="page_title">購物車</h1> <!-- 直譯 Cart 為 "大車" (亦可改為 購物車) -->

    <div class="cart_container" v-if="cartItems.length > 0">
      
      <!-- Left Column: Product List -->
      <div class="cart_items_area">
        <div 
          v-for="item in cartItems" 
          :key="item.id" 
          class="cart_item"
        >
          <!-- 商品圖片 -->
          <div class="item_image_col">
            <div class="img_placeholder">
               <!-- 這裡使用背景色模擬圖片，若有真實圖片可換 <img :src="item.image"> -->
               <img v-if="item.image" :src="item.image" :alt="item.title" @error="e => e.target.style.display='none'" />
            </div>
          </div>

          <!-- 商品資訊 -->
          <div class="item_info_col">
            <h2 class="item_title">{{ item.title }}</h2>
            <p class="item_variant">{{ item.variant }}</p>

            <!-- 數量選擇器 -->
            <div class="qty_control">
              <button class="qty_btn" @click="decreaseQty(item)" :disabled="item.quantity <= 1">-</button>
              <span class="qty_text">{{ item.quantity }}</span>
              <button class="qty_btn" @click="increaseQty(item)">+</button>
            </div>

            <!-- 移除按鈕 -->
            <button class="remove_btn" @click="removeItem(item.id)">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </div>

          <!-- 單項總價 -->
          <div class="item_price_col">
            <span class="price_text">{{ formatPrice(item.price * item.quantity) }}</span>
          </div>
        </div>
      </div>

      <!-- Right Column: Order Summary (Sticky) -->
      <div class="cart_summary_area">
        <div class="summary_card">
          <NuxtLink to="/products" class="summary_header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            <span>返回商店</span>
          </NuxtLink>

          <div class="summary_info_block">
             <div class="summary_row">
               <span>數量</span>
               <span>{{ totalQuantity }} 件</span>
             </div>
             <div class="summary_row">
               <span>小計</span>
               <span>{{ formatPrice(subtotal) }}</span>
             </div>
             <div class="summary_row">
               <span>運費</span>
               <span>{{ formatPrice(shippingFee) }}</span>
             </div>
          </div>
          


          <hr class="summary_divider">

          <div class="summary_total">
            <span>總金額</span>
            <span class="total_price">{{ formatPrice(totalAmount) }}</span>
          </div>

          <!-- Checkout Button -->
          <button class="checkout_btn" @click="checkout">
            結帳
          </button>

          <!-- Payment Icons -->
          <div class="payment_icons">
            <div class="pay_icon shop_pay">shop</div>
            <div class="pay_icon paypal">PayPal</div>
            <div class="pay_icon gpay"><span class="g">G</span> Pay</div>
          </div>

          <!-- Shipping Notice -->
          <div class="shipping_notice">
            <p>全台皆可運送</p>
            <p>皆採宅配 (出貨後隔天到達，週日貨運無營業順延周一)</p>
            <p class="highlight">※ 東部區域可能會晚 1-2 天到達</p>
          </div>

          <!-- Continue Shopping -->
          <button class="continue_btn" @click="continueShopping">
            繼續購物
          </button>

        </div>
      </div>

    </div>

    <!-- Empty State -->
    <div v-else class="empty_cart">
      <p>購物車目前是空的</p>
      <button class="continue_btn" @click="continueShopping" style="max-width: 200px;">去逛逛</button>
    </div>

  </div>
</template>

<style scoped>
/* 全局設定 */
.cart_page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
  color: #333;
  font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
}

.page_title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 60px;
  letter-spacing: 0.1em;
  font-weight: 500;
}

/* 佈局容器 Flexbox */
.cart_container {
  display: flex;
  gap: 60px;
  align-items: flex-start;
}

/* 左側：商品列表 */
.cart_items_area {
  flex: 65%; /* 佔寬度 65% */
}

.cart_item {
  display: flex;
  border-bottom: 1px solid #eee; /* 分隔線 */
  padding-bottom: 40px;
  margin-bottom: 40px;
}

/* 圖片區 */
.item_image_col {
  width: 120px;
  margin-right: 30px;
  flex-shrink: 0;
}

.img_placeholder {
  width: 100%;
  aspect-ratio: 1;
  background-color: #e8dcd2; /* 模擬圖中的米色背景 */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.img_placeholder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 資訊區 */
.item_info_col {
  flex-grow: 1;
}

.item_title {
  font-size: 1.1rem;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.item_variant {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 20px;
}

/* 數量控制器 */
.qty_control {
  display: inline-flex;
  border: 1px solid #ddd;
  height: 36px;
  align-items: center;
  margin-bottom: 15px;
  background-color: #fff;
}

.qty_btn {
  width: 36px;
  height: 100%;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty_btn:disabled {
  color: #ccc;
  cursor: default;
}

.qty_text {
  min-width: 30px;
  text-align: center;
  font-size: 0.95rem;
}

.remove_btn {
  display: block;
  background: none;
  border: none;
  text-decoration: none; /* No underline for icon */
  color: #999; /* Softer color for icon */
  font-size: 0.9rem;
  cursor: pointer;
  padding: 5px; /* Increase touch target slightly */
  margin-top: 5px;
  transition: all 0.2s ease;
}

.remove_btn:hover {
  color: #000;
}

/* 價格區 (單品總價) */
.item_price_col {
  text-align: right;
  min-width: 100px;
  display: flex;
  align-items: flex-end; /* 讓價格靠下對齊，模擬圖中效果 */
  justify-content: flex-end;
  padding-bottom: 5px;
}

.price_text {
  font-size: 1.1rem;
  letter-spacing: 0.05em;
  font-weight: 500;
}


/* 右側：訂單摘要 */
.cart_summary_area {
  flex: 35%; /* 佔寬度 35% */
  position: sticky;
  top: 100px; /* 捲動時黏在頂部距離 100px 處 */
  background-color: #f9f9f9; /* 淺灰背景 */
  padding: 30px;
}

.summary_card {
  width: 100%;
}

.summary_header {
  font-size: 0.85rem;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
  margin-left: -5px; /* Move slightly left */
  margin-top: -10px; /* Move slightly up */
}

.summary_header:hover {
  color: #000;
  transform: translateX(-3px); /* Shift left slightly on hover */
}

.summary_info_block {
    margin-bottom: 20px;
}

.summary_row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    font-size: 0.95rem;
    color: #333;
}

.summary_divider {
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
}

.summary_total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.summary_total span:first-child {
    font-size: 1.1rem;
    font-weight: bold;
}

.total_price {
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #333;
}

/* 運費資訊 */
.shipping_info {
  margin-bottom: 25px;
  font-size: 0.85rem;
  color: #555;
  border-bottom: 1px dotted #ccc;
  padding-bottom: 20px;
}

.shipping_title {
  margin-bottom: 10px;
  font-weight: bold;
}

.shipping_row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.shipping_note {
  font-size: 0.75rem;
  color: #999;
  line-height: 1.4;
}

/* 按鈕群組 */
.checkout_btn {
  width: 100%;
/* 1. Update checkout button color */
  background-color: #dcd0ff; /* Light purple */
  color: #333;
  border: none;
  padding: 15px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 15px;
  border-radius: 4px;
  transition: opacity 0.2s;
}

.checkout_btn:hover {
  opacity: 0.8;
}

/* 付款圖示區 */
.payment_icons {
  display: flex;
  gap: 5px;
  margin-bottom: 15px;
}

.pay_icon {
  flex: 1;
  height: 40px;
  background-color: #5a31f4; /* Shop Pay 紫色 */
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
}

.pay_icon.paypal {
  background-color: #ffc439; /* PayPal 黃色 */
  color: #253b80;
}

.pay_icon.gpay {
  background-color: #000; /* GPay 黑色 */
  color: #fff;
}
.pay_icon.gpay .g {
  margin-right: 2px;
}

/* 運送須知 */
.shipping_notice {
  margin-bottom: 20px;
  font-size: 0.85rem;
  color: #555;
  line-height: 1.6;
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #eee;
}

.shipping_notice p {
    margin-bottom: 4px;
    margin-top: 0;
}

.shipping_notice .highlight {
    color: #888;
    font-size: 0.8rem;
    margin-bottom: 0;
}

/* 繼續購物按鈕 */
.continue_btn {
  width: 100%;
  background-color: #fff;
  border: 1px solid #333;
  color: #333;
  padding: 12px;
  font-size: 0.9rem;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
}

.continue_btn:hover {
  background-color: #f0f0f0;
}

.empty_cart {
  text-align: center;
  padding: 100px 0;
  color: #999;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* RWD: Mobile Breakpoint */
@media (max-width: 900px) {
  .cart_container {
    flex-direction: column; /* 轉為垂直排列 */
    gap: 40px;
  }
  
  .cart_items_area,
  .cart_summary_area {
    flex: auto;
    width: 100%;
  }

  .cart_summary_area {
    position: static; /* 手機版不黏貼 */
    margin-top: 20px;
  }
}
</style>
