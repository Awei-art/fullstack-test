<script setup>
import { computed } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

const isMiniCartOpen = computed(() => cartStore.isMiniCartOpen)
const cartItems = computed(() => cartStore.items)
const subtotal = computed(() => cartStore.totalPrice)
const totalQuantity = computed(() => cartStore.totalQty)

// 關閉小購物車
const closeCart = () => {
  cartStore.closeMiniCart()
}

// 跳轉至完整購物車結帳頁
const goToCart = () => {
  cartStore.closeMiniCart()
  router.push('/cart')
}

// 格式化金額
const formatPrice = (price) => {
  if (!price) return '0'
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// 移除商品
const removeItem = (key) => {
  cartStore.removeFromCart(key)
}

// 增加 / 減少數量
const increaseQty = (item) => {
  if (item.quantity < item.maxStock) {
    item.quantity++
    cartStore.saveToLocalStorage()
  } else {
    alert(`此商品目前庫存只剩 ${item.maxStock} 件`)
  }
}

const decreaseQty = (item) => {
  if (item.quantity > 1) {
    item.quantity--
    cartStore.saveToLocalStorage()
  }
}
</script>

<template>
  <div>
    <!-- 遮罩 (維持存在為了點擊可以關閉，但背景變透明不變黑) -->
    <div 
      v-show="isMiniCartOpen" 
      class="mini_cart_overlay" 
      @click="closeCart"
    ></div>

    <!-- 小購物車側邊欄 (改為下拉特效) -->
    <transition name="slide-down">
      <div v-show="isMiniCartOpen" class="mini_cart_drawer">
        <!-- 標頭 -->
        <div class="drawer_header">
          <h3>購物車 ({{ totalQuantity }})</h3>
          <button class="close_btn" @click="closeCart">✕</button>
        </div>

        <!-- 內容區 -->
        <div class="drawer_content">
          <div v-if="cartItems.length > 0" class="mini_items">
            <div 
              v-for="item in cartItems" 
              :key="item.key" 
              class="mini_item"
            >
              <div class="mini_img_wrap">
                <img :src="item.image" :alt="item.name" @error="e => e.target.style.display='none'">
              </div>
              <div class="mini_info">
                <h4>{{ item.name }}</h4>
                <p class="mini_variant" v-if="item.gradeName">【{{ item.gradeName }}】</p>
                <div class="mini_price">NT$ {{ formatPrice(item.price) }}</div>
                
                <div class="mini_qty_actions">
                  <div class="qty_control">
                    <button @click="decreaseQty(item)" :disabled="item.quantity <= 1">-</button>
                    <span>{{ item.quantity }}</span>
                    <button @click="increaseQty(item)" :disabled="item.quantity >= item.maxStock">+</button>
                  </div>
                  <button class="remove_line_btn" @click="removeItem(item.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      <line x1="10" y1="11" x2="10" y2="17"></line>
                      <line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty_mini_cart">
            <p>購物車是空的</p>
          </div>
        </div>

        <!-- 底部結帳按鈕區 -->
        <div class="drawer_footer" v-if="cartItems.length > 0">
          <div class="drawer_subtotal">
            <span>小計</span>
            <span class="subtotal_price">NT$ {{ formatPrice(subtotal) }}</span>
          </div>
          <p class="shipping_hint">運費將於結帳時計算</p>
          <button class="btn_go_checkout" @click="goToCart">
            前往結帳區
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* 遮罩 */
.mini_cart_overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: transparent; /* 背景不用變黑 */
  z-index: 1000;
}

/* 側邊菜單主體 */
.mini_cart_drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  max-width: 400px;
  height: 100vh;
  background-color: #fff;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 15px rgba(0,0,0,0.1);
}

.drawer_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.drawer_header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.close_btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  transition: color 0.3s ease;
}

.close_btn:hover {
  color: #000;
}

/* 中間列表區 */
.drawer_content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.empty_mini_cart {
  text-align: center;
  padding-top: 50px;
  color: #999;
}

.mini_item {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  padding-bottom: 25px;
  border-bottom: 1px dotted #ccc;
}

.mini_img_wrap {
  width: 80px;
  height: 80px;
  background: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.mini_img_wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mini_info {
  flex: 1;
}

.mini_info h4 {
  margin: 0 0 5px 0;
  font-size: 1rem;
  color: #333;
}

.mini_variant {
  font-size: 0.85rem;
  color: #777;
  margin: 0 0 8px 0;
}

.mini_price {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
  margin-bottom: 10px;
}

.mini_qty_actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.qty_control {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.qty_control button {
  background: #fff;
  border: none;
  width: 25px;
  height: 25px;
  cursor: pointer;
  color: #666;
}

.qty_control button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.qty_control span {
  font-size: 0.9rem;
  width: 30px;
  text-align: center;
}

.remove_line_btn {
  background: none;
  border: none;
  color: #999;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.2s ease;
}

.remove_line_btn:hover {
  color: #000;
}

/* 底部結帳區 */
.drawer_footer {
  padding: 20px;
  border-top: 1px solid #eee;
  background-color: #fafafa;
}

.drawer_subtotal {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.1rem;
  margin-bottom: 10px;
  color: #333;
}

.subtotal_price {
  font-weight: bold;
  font-size: 1.3rem;
}

.shipping_hint {
  font-size: 0.8rem;
  color: #777;
  text-align: center;
  margin-bottom: 15px;
}

.btn_go_checkout {
  width: 100%;
  padding: 15px;
  background-color: #dcd0ff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn_go_checkout:hover {
  opacity: 0.8;
}

/* 動畫設定 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.slide-down-enter-active, .slide-down-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-down-enter-from, .slide-down-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
