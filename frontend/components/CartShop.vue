<script setup>
import { computed } from 'vue'
// 1. 引入我們做好的 store
import { useCartStore } from '@/stores/cart'

// 設定 API URL
const config = useRuntimeConfig()
const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient

// 呼叫後端 API 取得最新商品與庫存資料
const { data: products } = await useFetch('/products/', {
  baseURL: baseURL,
  key: 'cart-products',
  default: () => []
})
const { data: desserts } = await useFetch('/desserts/', {
  baseURL: baseURL,
  key: 'cart-desserts',
  default: () => []
})

// 2. 初始化 store
const cartStore = useCartStore()

// 初始化 rawCartItems，對應原先的 store items
const rawCartItems = computed(() => cartStore.items)

// 結合即時的產品資料，確認購物車內商品使否有效（有庫存且品種未關閉）
const cartItems = computed(() => {
  if (!products.value || !desserts.value || (products.value.length === 0 && desserts.value.length === 0)) {
    return rawCartItems.value.map(item => ({ ...item, isValid: true, statusText: '' }))
  }

  return rawCartItems.value.map(item => {
    let isValid = true
    let statusText = ''
    let latestMaxStock = item.maxStock

    let latestProduct = null
    
    // 支援舊版 localStorage 裡存的字串 ID (例如 "dessert-1")
    let realId = item.id
    let safeItemType = item.itemType || 'product'
    
    if (typeof realId === 'string') {
      if (realId.startsWith('dessert-')) safeItemType = 'dessert'
      realId = parseInt(realId.replace(/^(dessert-|product-)/, ''))
    }

    // 將修復後的型別塞回去，以免後續出錯
    item.itemType = safeItemType

    if (safeItemType === 'dessert') {
      latestProduct = desserts.value?.find(d => d.id === realId)
    } else {
      latestProduct = products.value?.find(p => p.id === realId)
    }

    if (!latestProduct) {
      isValid = false
      statusText = '已下架'
    } else {
      // 檢查等級庫存或總庫存
      if (item.gradeId) {
        const safeGradeId = typeof item.gradeId === 'string' ? parseInt(item.gradeId) : item.gradeId
        const grade = latestProduct.grades?.find(g => g.id === safeGradeId)
        if (grade) {
          latestMaxStock = grade.stock
          if (grade.stock <= 0) isValid = false
        } else {
          isValid = false
          statusText = '等級已停售'
        }
      } else {
        latestMaxStock = latestProduct.stock
        if (latestProduct.stock <= 0) isValid = false
      }

      // 檢查品種是否全都有開放 (葡萄專用)
      if (safeItemType !== 'dessert' && isValid && item.varieties && item.varieties.length > 0) {
        const activeVarietyIds = latestProduct.varieties ? latestProduct.varieties.map(v => v.id) : []
        const hasClosedVariety = item.varieties.some(v => !activeVarietyIds.includes(v.id))
        
        if (hasClosedVariety) {
          isValid = false
        }
      }
      
      // 如果上述檢查為不合法，設定為補貨中
      if (!isValid && !statusText) {
        statusText = '補貨中'
      }
    }

    return {
      ...item,
      isValid,
      statusText,
      maxStock: latestMaxStock // 覆蓋成最新庫存
    }
  })
})

const validCartItems = computed(() => cartItems.value.filter(item => item.isValid))

const subtotal = computed(() => {
  return validCartItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const totalQuantity = computed(() => {
  return validCartItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

// 系統自動計算的大購物車預設最終運費 (以 1 個地址作為結帳基準)
const shippingFee = computed(() => {
  const totalBoxes = totalQuantity.value
  const tPrice = subtotal.value
  if (totalBoxes === 0) return 0
  
  const avgPrice = tPrice / totalBoxes
  let packages = []
  let remainBoxes = totalBoxes
  
  // 1個地址的情況，每4盒拆一包
  while (remainBoxes > 0) {
    const pkgBoxes = Math.min(4, remainBoxes)
    packages.push(pkgBoxes)
    remainBoxes -= pkgBoxes
  }

  // 對每一包計算運費（箱數 或 金額門檻，擇一符合即套用，不重複）
  let fees = packages.map(pkgBoxes => {
    const pkgPrice = pkgBoxes * avgPrice
    if (pkgBoxes >= 4 || pkgPrice >= 2500) return 0
    if (pkgBoxes >= 2 || pkgPrice >= 1250) return 150
    return 230
  })

  // 滿額優惠：兩種免運來源取較多者（不重複疊加）
  //  - 箱數優惠：總箱數 ≥ 10 → ceil(箱數/4) 個免運
  //  - 金額優惠：每滿 $2,500 → 免 1 個包裹
  const boxFreeCount = totalBoxes >= 10 ? Math.ceil(totalBoxes / 4) : 0
  const priceFreeCount = Math.floor(tPrice / 2500)
  const freeCount = Math.max(boxFreeCount, priceFreeCount)

  if (freeCount > 0) {
    for (let i = 0; i < Math.min(freeCount, fees.length); i++) {
      fees[i] = 0
    }
  }

  return fees.reduce((sum, fee) => sum + fee, 0)
})

// 包裹拆分資訊（幾個包裹、幾個免運）
const packageInfo = computed(() => {
  const totalBoxes = totalQuantity.value
  if (totalBoxes === 0) return { total: 0, free: 0 }

  const avgPrice = subtotal.value / totalBoxes
  let packages = []
  let remainBoxes = totalBoxes

  while (remainBoxes > 0) {
    const pkgBoxes = Math.min(4, remainBoxes)
    packages.push(pkgBoxes)
    remainBoxes -= pkgBoxes
  }

  // 計算每包是否免運
  let fees = packages.map(pkgBoxes => {
    const pkgPrice = pkgBoxes * avgPrice
    if (pkgBoxes >= 4 || pkgPrice >= 2500) return 0
    if (pkgBoxes >= 2 || pkgPrice >= 1250) return 150
    return 230
  })

  const boxFree = totalBoxes >= 10 ? Math.ceil(totalBoxes / 4) : 0
  const priceFree = Math.floor(subtotal.value / 2500)
  const freeCount = Math.max(boxFree, priceFree)

  if (freeCount > 0) {
    for (let i = 0; i < Math.min(freeCount, fees.length); i++) {
      fees[i] = 0
    }
  }

  const freePackages = fees.filter(f => f === 0).length
  return { total: packages.length, free: freePackages }
})

// 總金額 (小計 + 運費)
const totalAmount = computed(() => {
  return subtotal.value + shippingFee.value
})

// 格式化金額 (千分位)
const formatPrice = (price) => {
  return 'NT$ ' + price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// 增加數量
const increaseQty = (mappedItem) => {
  const item = cartStore.items.find(i => i.key === mappedItem.key)
  if (!item) return
  // 檢查是否超過該商品的最高庫存
  if (item.quantity < mappedItem.maxStock) {
    item.quantity++
    cartStore.saveToLocalStorage() // 數字改變，記得存檔
  } else {
    alert(`此商品目前庫存只剩 ${mappedItem.maxStock} 件`)
  }
}

// 減少數量
const decreaseQty = (mappedItem) => {
  const item = cartStore.items.find(i => i.key === mappedItem.key)
  if (!item) return
  if (item.quantity > 1) {
    item.quantity--
    cartStore.saveToLocalStorage() // 數字改變，記得存檔
  }
}

// 移除商品
const removeItem = (key) => {
  if (confirm('確定要移除這個商品嗎？')) {
    cartStore.removeFromCart(key)
  }
}

// 繼續購物
const continueShopping = () => {
  navigateTo('/products')
}

// 結帳
const checkout = () => {
  if (validCartItems.value.length === 0) {
    alert('購物車內目前沒有可結帳的商品')
    return
  }
  navigateTo('/checkout')
}
</script>

<template>
  <div class="cart_page">
    <h1 class="page_title">購物車</h1>

    <ClientOnly>
    <div class="cart_container" v-if="cartItems.length > 0">
      
      <div class="cart_items_area">
        <div 
          v-for="item in cartItems" 
          :key="item.key" 
          class="cart_item"
          :class="{ 'out_of_stock_item': !item.isValid }"
        >
          <div class="item_image_col">
            <div class="img_placeholder">
               <img v-if="item.image" :src="item.image" :alt="item.name" @error="e => e.target.style.display='none'" />
            </div>
          </div>

          <div class="item_info_col">
            <h2 class="item_title">
              {{ item.name }}
              <span v-if="!item.isValid" class="status_badge">{{ item.statusText }}</span>
            </h2>
            
            <p class="item_variant">
              <span v-if="item.gradeName">【{{ item.gradeName }}】</span>
              <span v-if="item.varieties && item.varieties.length > 0">
                內容物：{{ item.varieties.map(v => v.name).join(' + ') }}
              </span>
            </p>

            <div class="qty_control" :class="{ 'disabled_area': !item.isValid }">
              <button class="qty_btn" @click="decreaseQty(item)" :disabled="item.quantity <= 1 || !item.isValid">-</button>
              <span class="qty_text">{{ item.quantity }}</span>
              <button class="qty_btn" @click="increaseQty(item)" :disabled="item.quantity >= item.maxStock || !item.isValid">+</button>
            </div>

            <button class="remove_btn" @click="removeItem(item.key)">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </div>

          <div class="item_price_col">
            <span class="price_text">{{ formatPrice(item.price * item.quantity) }}</span>
          </div>
        </div>
      </div>

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
             <p class="package_hint" v-if="totalQuantity > 0">
               📦 共 {{ packageInfo.total }} 件包裹，{{ packageInfo.free }} 件免運
               <span v-if="packageInfo.total - packageInfo.free > 0">、{{ packageInfo.total - packageInfo.free }} 件需付運費</span>
             </p>
          </div>
          
          <hr class="summary_divider">

          <div class="summary_total">
            <span>總金額</span>
            <span class="total_price">{{ formatPrice(totalAmount) }}</span>
          </div>

          <button class="checkout_btn" @click="checkout" :disabled="validCartItems.length === 0" :class="{ 'btn-disabled': validCartItems.length === 0 }">
            結帳
          </button>



          <div class="shipping_notice">
            <p>全台皆可運送</p>
            <p>皆採宅配 (出貨後隔天到達，週日貨運無營業順延周一)</p>
            <p class="highlight">※ 東部區域可能會晚 1-2 天到達</p>
          </div>

          <!-- 加入智能多地址運費計算機元件 (僅供試算，不連動最終結帳金額) -->
          <ShippingCalculator 
            :totalBoxes="totalQuantity" 
            :totalPrice="subtotal" 
          />

          <button class="continue_btn" @click="continueShopping">
            繼續購物
          </button>

        </div>
      </div>
    </div>

    <div v-else class="empty_cart">
      <p>購物車目前是空的</p>
      <button class="continue_btn" @click="continueShopping" style="max-width: 200px;">去逛逛</button>
    </div>
</ClientOnly>

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
  display: flex;
  align-items: center;
  gap: 10px;
}

.status_badge {
  font-size: 0.8rem;
  color: #e74c3c;
  background: #fdf0ed;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.out_of_stock_item {
  color: #999;
}

.out_of_stock_item .img_placeholder img {
  filter: grayscale(100%);
  opacity: 0.6;
}

.out_of_stock_item .item_title, 
.out_of_stock_item .item_variant,
.out_of_stock_item .price_text {
  color: #aaa;
}

.disabled_area {
  opacity: 0.5;
  pointer-events: none;
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

.package_hint {
    font-size: 0.8rem;
    color: #888;
    margin: -4px 0 0 0;
    line-height: 1.4;
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

.checkout_btn:hover:not(:disabled) {
  opacity: 0.8;
}

.checkout_btn:disabled {
  background-color: #eee;
  color: #999;
  cursor: not-allowed;
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
