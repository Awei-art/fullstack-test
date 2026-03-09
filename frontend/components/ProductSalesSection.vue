<script setup>
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

// 1. 設定後端 API 網址
const config = useRuntimeConfig()
const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient

// 接收父頁面的分類篩選
const activeCategory = inject('activeCategory', ref(null))
const activeColor = inject('activeColor', ref(null))

// 2. 抓取資料（支援分類 + 顏色篩選）
const { data: products, pending, error, execute } = await useFetch('/products/', {
  baseURL: baseURL,
  key: 'sales-products',
  default: () => [],
  query: computed(() => {
    const q = {}
    if (activeCategory.value) q.category = activeCategory.value
    if (activeColor.value) q.color = activeColor.value
    return q
  }),
  watch: false // 關閉預設的 watch，我們自己手動控制
})

// 確實監聽分類與顏色的變化，然後強制發送新 Request
watch([activeCategory, activeColor], () => {
  execute()
}, { deep: true })

// 3. 處理金額千分位 (例如 1200 變 1,200)
const formatPrice = (price) => {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// 例如：資料庫是 4.00 -> 顯示 4；資料庫是 1.5 -> 顯示 1.5
const formatNumber = (num) => {
    return parseFloat(num)
}


// 4. 判斷單一商品是否售完
const checkSoldOut = (product) => {
  // Step 1: 先判斷「物理庫存」是否有貨
  let hasStock = false;

  // 如果有分等級，計算等級總庫存
  if (product.grades && product.grades.length > 0) {
    const totalGradeStock = product.grades.reduce((sum, grade) => sum + grade.stock, 0);
    hasStock = totalGradeStock > 0;
  } 
  // 如果沒分等級，看一般庫存
  else {
    hasStock = product.stock > 0;
  }

  // 🔴 第一關：如果連物理庫存都沒有，直接判斷售完
  if (!hasStock) return true;


  // Step 2: 再判斷「品種開關」是否開啟 (軟體限制)
  // (這一步非常重要！必須在庫存檢查之後執行)
  
  // 取得目前後端回傳「有開關且活著」的品種數量
  const activeCount = product.varieties ? product.varieties.length : 0;
  
  // 取得這款禮盒需要的數量 (預設為 1)
  const requiredCount = product.mix_limit || 1;

  // 🔴 第二關：如果「活著的品種」少於「需要的數量」，也算售完！
  // (例如：巨峰S級有庫存，但巨峰品種被關掉 -> activeCount為0 -> 售完)
  if (activeCount < requiredCount) return true;


  // 🟢 兩關都過了，才代表真的有貨
  return false;
}

// 5. 處理圖片路徑 (解決 SSR 與上線部署後的路徑問題)
const getImageUrl = (url) => {
    if (!url) return '/images/default-grape.png'
    
    // 從 config 抓取前端呼叫 API 的設定
    const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '')

    if (url.startsWith('http://backend:8000')) {
        return url.replace('http://backend:8000', clientBaseUrl)
    }
    if (url.startsWith('/media/')) {
        return `${clientBaseUrl}${url}`
    }
    return url
}

// 6. 加入購物車功能 (無縫接軌 ProductDetail)
const addToCart = (product) => {
  if (checkSoldOut(product)) return

  // 🔥 解決圖片路徑問題
  let safeImage = getImageUrl(product.image)

  // 嘗試取得預設等級 (如果有的話)
  let currentGrade = null
  let displayStock = product.stock
  if (product.grades && product.grades.length > 0) {
    // 找一個有庫存的等級
    currentGrade = product.grades.find(g => g.stock > 0) || product.grades[0]
    displayStock = currentGrade.stock
  }

  // 嘗試預設選擇品種 (滿足 mix_limit 需求)
  let selectedVarieties = []
  const limit = product.mix_limit || 1
  if (product.varieties && product.varieties.length > 0) {
    // 直選前 N 個有庫存活著的品種來湊數
    selectedVarieties = product.varieties.slice(0, limit)
  }

  // 整理要存進購物車的資料
  const cartItem = {
    itemType: 'product',
    id: product.id,
    name: product.name,
    image: safeImage,
    price: currentGrade ? currentGrade.price : product.price,
    quantity: 1, // 列表頁一律每次加 1
    gradeId: currentGrade ? currentGrade.id : null,
    gradeName: currentGrade ? currentGrade.name : null,
    varieties: selectedVarieties.map(v => ({ id: v.id, name: v.name })),
    maxStock: displayStock 
  }

  // 呼叫 Store 的動作
  const success = cartStore.addToCart(cartItem)

  // 只有成功加入時，才會彈出小購物車
  if (success) {
    cartStore.openMiniCart()
  }
}
</script>

<template>
  <section class="grape_sales_section">
    <div class="grape_sales_container">

      <div v-if="pending">載入中...</div>
      
      <div v-else-if="error">資料載入失敗，請稍後再試</div>

      <div v-else class="product_grid">
        <div 
          v-for="product in products" 
          :key="product.id" 
          class="product_card"
          :class="{ 'sold-out': checkSoldOut(product) }" 
        >
          <div class="product_img_wrap">
            <span class="product_badge">
                {{ formatNumber(product.unit_value) }}{{ product.unit_name }} / 盒 
            </span> 
            
            <NuxtLink :to="`/products/${product.id}`" style="display: block; width: 100%; height: 100%;">
              <img 
                :src="getImageUrl(product.image)" 
                :alt="product.name" 
                class="product_img"
              >
            </NuxtLink>
            
            <div v-if="checkSoldOut(product)" class="sold-out-overlay">
              已售完
            </div>
          </div>

            <div class="product_info">
            <h3 class="product_name">{{ product.name }}</h3>
            <p class="product_desc">{{ product.description }}</p>

            <div class="product_price">
              <small>NT$</small>{{ formatPrice(product.price) }}
            </div>
            
            <div class="product_footer">
              <NuxtLink :to="`/products/${product.id}`" class="btn_view_product" style="text-decoration: none; display: flex; justify-content: center; align-items: center;">
                商品詳情
              </NuxtLink>

              <button 
                class="btn_add_cart" 
                :disabled="checkSoldOut(product)"
                :class="{ 'btn-disabled': checkSoldOut(product) }"
                @click.prevent="addToCart(product)"
              >
                <i class="fas fa-cart-plus"></i> 
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style src="@/assets/css/ProductSalesSection.css" scoped></style>
