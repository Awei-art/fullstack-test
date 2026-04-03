<script setup>
import { ref, computed, watchEffect, reactive } from 'vue'

// ==========================================
// 購物車邏輯
// ==========================================
// 1. 引入剛剛寫好的 store
import { useCartStore } from '@/stores/cart'

// 2. 初始化 store
const cartStore = useCartStore()
// ==========================================

const route = useRoute()
// 1. 設定後端 API 網址
const config = useRuntimeConfig()
const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient

// 2. 呼叫後端 API
const { data: product, pending } = await useFetch(`/products/${route.params.id}/`, {
  baseURL: baseURL,
  key: `product-detail-${route.params.id}`,
  lazy: true
})

// 處理圖片路徑 (解決 SSR 與上線部署後的路徑問題，包含 Cloudinary 加速)
const getImageUrl = (url) => {
    if (!url) return null

    // Cloudinary 優化：自動壓縮與轉成 WebP
    if (typeof url === 'string' && url.includes('res.cloudinary.com') && url.includes('/image/upload/')) {
        if (!url.includes('f_auto') && !url.includes('q_auto')) {
            url = url.replace('/image/upload/', '/image/upload/f_auto,q_auto/')
        }
    }

    const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '')

    if (url.startsWith('http://backend:8000')) {
        return url.replace('http://backend:8000', clientBaseUrl)
    }
    if (url.startsWith('/media/')) {
        return `${clientBaseUrl}${url}`
    }
    return url
}

// ==========================================
// 圖片處理邏輯
// ==========================================
const galleryImages = computed(() => {
  if (!product.value) return []
  const list = []
  
  // 1. 封面圖
  if (product.value.image) list.push(getImageUrl(product.value.image))
  
  // 2. 相簿圖 (後端回傳的是物件陣列，要取出 image 欄位)
  if (product.value.images && product.value.images.length > 0) {
    product.value.images.forEach(imgObj => {
      list.push(getImageUrl(imgObj.image))
    })
  }
  
  // 3. 防呆預設圖
  if (list.length === 0) list.push('/images/default-grape.png')
  
  return list
})

const currentImage = ref('')

// 自動設定第一張圖
watchEffect(() => {
  if (galleryImages.value.length > 0) {
    // 如果沒選圖，或選的圖不在清單內，就預設第一張
    if (!currentImage.value || !galleryImages.value.includes(currentImage.value)) {
      currentImage.value = galleryImages.value[0]
    }
  }
})

const changeImage = (imgSrc) => {
  currentImage.value = imgSrc
}

// ==========================================
// 品種選擇邏輯 (混合禮盒專用)
// ==========================================
// 1. 🔥 狀態改變：從單一變數 (null) 改成 空陣列 ([])
const selectedVarieties = ref([]) 

// 2. 🔥 點擊邏輯改變：從「替換」改成「切換 (Toggle)」
// 這裡可以傳入 maxLimit 參數限制最多選幾種 (例如雙色禮盒 maxLimit = 2)
const toggleVariety = (variety) => {
  const limit = product.value.mix_limit || 1
  const index = selectedVarieties.value.findIndex(item => item.id === variety.id)

  if (limit === 1) {
    // 單品種模式：切換時直接替換，且點擊已選中的不動作 (達成無法取消選擇)
    if (index === -1) {
      selectedVarieties.value = [variety]
    }
    return
  }

  // 多品種模式 (mix_limit > 1)：正常 Toggle
  if (index > -1) {
    selectedVarieties.value.splice(index, 1)
  } else {
    if (selectedVarieties.value.length < limit) {
      selectedVarieties.value.push(variety)
    }
  }
}

// 3. 🔥 預設與防呆監聽：當產品資料載入或變動時執行
watchEffect(() => {
  // 確認產品存在且有品種列表
  if (product.value && product.value.varieties && product.value.varieties.length > 0) {
    const limit = product.value.mix_limit || 1
    
    // A. 🔥 預設選擇邏輯：
    // 如果是「單品種禮盒 (limit=1)」，幫他預選第一個；
    // 如果是「多品種禮盒 (limit>1)」，則不預選 (length === 0)
    if (selectedVarieties.value.length === 0 && limit === 1) {
      selectedVarieties.value = [product.value.varieties[0]]
      return 
    }

    // B. 資料效度檢查：確保「已選名單」裡的品種都是活著的
    const validIds = product.value.varieties.map(v => v.id)
    const newSelection = selectedVarieties.value.filter(selected => validIds.includes(selected.id))

    if (newSelection.length !== selectedVarieties.value.length) {
      selectedVarieties.value = newSelection
    }

  } else {
    // 如果沒有資料，清空選擇
    selectedVarieties.value = []
  }
})

// 4. 輔助函式：給 Template 判斷樣式用
// 檢查某個 ID 是否在已選陣列中
const isSelected = (varietyId) => {
  return selectedVarieties.value.some(item => item.id === varietyId)
}
// ==========================================
// 等級選擇邏輯
// ==========================================
const currentGrade = ref(null)

// 資料載入時，自動選擇第一個等級
watchEffect(() => {
  if (product.value && product.value.grades && product.value.grades.length > 0) {
    // 如果還沒選，預設選第一個 (通常是 S級)
    if (!currentGrade.value) {
      currentGrade.value = product.value.grades[0]
    }
  }
})

const selectGrade = (grade) => {
  currentGrade.value = grade
  // 切換等級時，記得把購買數量重置為 1，以免超過新等級的庫存
  quantity.value = 1
}

// ==========================================
// 🔥 計算最終顯示的價格與庫存
// ==========================================
const displayPrice = computed(() => {
  // 如果有選等級，顯示等級價；否則顯示原本商品價
  if (currentGrade.value) {
    return currentGrade.value.price
  }
  return product.value?.price || 0
})

const displayStock = computed(() => {
  // 如果有選等級，顯示等級庫存；否則顯示原本商品庫存
  if (currentGrade.value) {
    return currentGrade.value.stock
  }
  return product.value?.stock || 0
})

// ==========================================
// 數量與庫存邏輯
// ==========================================
// 1. 計算「總金額」 (單價 x 數量)
const totalAmount = computed(() => {
  return displayPrice.value * quantity.value
})

const quantity = ref(1)

const updateQty = (change) => {
  let val = quantity.value + change
  // 不能小於 1
  if (val < 1) val = 1
  // 不能大於庫存
  if (val > displayStock.value) val = displayStock.value
  quantity.value = val
}

const checkQty = (event) => {
  let val = parseInt(event.target.value)
  if (isNaN(val) || val < 1) val = 1
  // 檢查是否超過庫存
  // 改用 displayStock.value，這樣 S級跟 A級的上限就會不同
  if (val > displayStock.value) {
    val = displayStock.value
  }
  quantity.value = val
  event.target.value = val
}
// ==========================================
// 智慧售完
// ==========================================
// 判斷是否售完 (結合庫存 + 品種狀況)
const isSoldOut = computed(() => {
  if (!product.value) return true

  // =========================================
  // 1 優先檢查「等級庫存」
  // =========================================
  // 如果這個商品有設定等級 (例如 S級, A級)
  if (product.value.grades && product.value.grades.length > 0) {
    // 把所有等級的庫存加總
    const totalGradeStock = product.value.grades.reduce((sum, grade) => sum + grade.stock, 0)
    
    // 如果所有等級加起來是 0，那就是真的賣完了 (不需往下檢查)
    if (totalGradeStock <= 0) return true
  } 
  // =========================================
  // 2 如果沒有等級，才檢查「商品總庫存」
  // =========================================
  else {
    if (product.value.stock <= 0) return true
  }


  
  // =========================================
  // 3 檢查品種是否足夠 (軟體限制)
  // =========================================
  // (這部分邏輯保持不變，因為就算是 S級禮盒，如果品種不夠湊成三色，也是不能賣)
  const activeCount = product.value.varieties ? product.value.varieties.length : 0
  const requiredCount = product.value.mix_limit || 1

  if (activeCount < requiredCount) return true

  // 都通過，代表可以買
  return false
})
// ==========================================
// 格式化工具
// ==========================================
const formatPrice = (price) => {
  return price?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") || '0'
}

// ==========================================
// 手風琴 (保持原本邏輯)
// ==========================================
const accordionStates = reactive({
  important: true,
  shipping: true
})
const toggleAccordion = (key) => {
  accordionStates[key] = !accordionStates[key]
}

// ==========================================
// 購物車按鈕
// ==========================================
// 加入 skipOpen 參數，用來判斷是否需要跳過開啟右側購物車的動作 (例如點擊立即購買時)
const addToCart = (skipOpen = false) => {
  // 防呆：如果售完或未選滿品種就不執行
  const limit = product.value?.mix_limit || 1
  if (isSoldOut.value || selectedVarieties.value.length < limit) return


  // 🔥 解決圖片路徑問題：用 getImageUrl 統一處理
  let safeImage = getImageUrl(product.value.image) || '/images/default-grape.png'
  // 1. 整理要存進購物車的資料
  const cartItem = {
    itemType: 'product',
    id: product.value.id,
    name: product.value.name,
    image: safeImage, // 存圖片路徑，購物車頁面要顯示
    
    // 價格：如果有分等級，要存等級的價錢
    price: currentGrade.value ? currentGrade.value.price : product.value.price,
    
    // 數量
    quantity: quantity.value,

    // 規格資訊 (存下來是為了在購物車頁面顯示給客人看)
    gradeId: currentGrade.value ? currentGrade.value.id : null,
    gradeName: currentGrade.value ? currentGrade.value.name : null,
    
    // 品種：把選中的品種陣列存起來
    varieties: selectedVarieties.value ? selectedVarieties.value.map(v => ({ id: v.id, name: v.name })) : [],
    
    // 最大庫存限制 (讓購物車頁面也能檢查庫存)
    maxStock: displayStock.value 
  }

  // 2. 呼叫 Store 的動作 (如果 skipOpen 為 true，那就代表是立即購買，連同 Alert 也一併關閉)
  const success = cartStore.addToCart(cartItem, skipOpen)

  // 3. 只有成功加入時，且沒有被要求 skipOpen，才會彈出小購物車
  if (success && !skipOpen) {
    cartStore.openMiniCart()
  }
  
  // 回傳是否加入成功（給 buyNow 判斷用）
  return success
}

// ... (立即購買的邏輯) ...
const buyNow = () => {
    cartStore.closeMiniCart() // 先確保沒打開小購物車
    const added = addToCart(true) // 嘗試加購物車，傳入 true 表示跳過彈出視窗與警示
    
    if (added) {
      navigateTo('/cart') // 加入成功，跳轉去大結帳頁
    } else {
      // 加入失敗 (通常是因為已經達庫存上限)，即使 silent=true，我們也可選擇在這裡直接跳轉讓消費者在結帳頁看到數量
      navigateTo('/cart') 
    }
}

// 麵包屑導覽列
const breadcrumbs = computed(() => {
  if (!product.value) return []
  return [
    { name: '首頁', path: '/' },
    { name: '葡萄商店', path: '/products' },
    { name: product.value.name }
  ]
})

</script>

<template>
  <section class="product_detail_section">
    <!-- 麵包屑導覽列 -->
    <AppBreadcrumb v-if="product" :items="breadcrumbs" />

    <div class="product_detail_container" v-if="product">
      
      <div class="detail_gallery">
        <div class="main_image_wrap">
          <img :src="currentImage" :alt="product.name" class="main_image" id="mainImage">
          <div class="zoom_icon"><i class="fas fa-search-plus"></i></div>
        </div>
        
        <div class="thumbnail_list" v-if="galleryImages.length > 1">
          <div 
            v-for="(img, index) in galleryImages" 
            :key="index"
            class="thumb_item" 
            :class="{ active: currentImage === img }"
            @click="changeImage(img)"
          >
            <img :src="img" :alt="'Thumb ' + (index + 1)" class="thumb_img" loading="lazy">
          </div>
        </div>
      </div>

      <div class="detail_info">
        <span class="brand_tag">TIANYUAN GRAPE ~ PREMIUM SELECTION ~</span>
        
        <h1 class="detail_product_title">{{ product.name }}</h1>
        <hr class="product_title_divider">

        <div class="detail_price">
          NT${{ formatPrice(displayPrice) }} <span>(含稅)</span>
        </div>

        <div class="option_group" v-if="product.spec_display">
          <span class="option_label">規格選擇</span>
          <div class="size_grid">
            <div class="size_btn active">
              {{ product.spec_display }} </div>
            </div>
        </div>

        <div class="option_group" v-if="product.grades && product.grades.length > 0">
        <span class="option_label">等級選擇</span>
        <div class="grade_row">
          <div 
            v-for="grade in product.grades" 
            :key="grade.id"
            class="grade_btn" 
            :class="{ active: currentGrade?.id === grade.id }"
            @click="selectGrade(grade)"
          >
            {{ grade.name }}
          </div>
        </div>
      </div>

       <div class="option_group" v-if="product.varieties && product.varieties.length > 0">
    <span class="option_label">禮盒內容物 (目前供貨)</span>
    
    <div class="grade_row">
            <div 
            v-for="v in product.varieties" 
            :key="v.id"
            class   ="grade_btn"
            :class="{ active: isSelected(v.id) }"
            @click="toggleVariety(v)" 
            >
            {{ v.name }}
            </div>
    </div>

    <div class="selected_info" style="margin-top: 10px; color: #666; font-size: 14px;">
       已選擇：
       <span v-if="selectedVarieties.length === 0">尚未選擇</span>
       <span v-else>
         {{ selectedVarieties.map(v => v.name).join(' + ') }}
       </span>

       <span 
      v-if="selectedVarieties.length >= (product.mix_limit || 1)" 
      style="color: #e74c3c; margin-left: 8px; font-weight: bold;"
    >
      (數量已達上限)
    </span>
    </div>

  </div>

        <div class="option_group">
          <span class="option_label">運送方式</span>
          <button class="selected_shipping">
            黑貓冷藏宅配 (運費另計)
          </button>
          <a href="#" class="shipping_detail_link">運費詳情</a>
        </div>

        <div class="stock_display">
          庫存：<span id="stockCount">{{ isSoldOut ? 0 : displayStock }}</span> 件
        </div>

        <div class="quantity_wrap">
          <span class="quantity_label">數量</span>
          <div class="qty_selector">
            <button class="qty_btn minus" @click="updateQty(-1)" :disabled="quantity <= 1 || isSoldOut">-</button>
            
            <input 
              type="text" 
              :value="quantity" 
              class="qty_input" 
              id="qtyInput"
              :disabled="isSoldOut"
              @input="event => event.target.value = event.target.value.replace(/[^0-9]/g, '')" 
              @change="checkQty"
            >
            
            <button class="qty_btn plus" @click="updateQty(1)" :disabled="quantity >= displayStock || isSoldOut">+</button>
          </div>
        </div>

        <div class="action_buttons">
          <button 
            class="add_to_cart_btn" 
            @click="() => addToCart(false)" 
            :disabled="isSoldOut || displayStock === 0 || selectedVarieties.length < (product.mix_limit || 1)" 
            :class="{ 'btn-disabled': isSoldOut || displayStock === 0 || selectedVarieties.length < (product.mix_limit || 1)}"
            >   
            <template v-if="isSoldOut || displayStock === 0">已售完</template>
            <template v-else-if="selectedVarieties.length < (product.mix_limit || 1)">
              請選擇 {{ product.mix_limit || 1 }} 種品種
            </template>
            <template v-else>加入購物車</template>
            </button>
          <button 
            class="buy_now_btn" 
            @click="buyNow"
            :disabled="isSoldOut || displayStock === 0 || selectedVarieties.length < (product.mix_limit || 1)"
            :class="{ 'btn-disabled': isSoldOut || displayStock === 0 || selectedVarieties.length < (product.mix_limit || 1)}"
          >
            立即購買
          </button>
        </div>

        <div class="accordion_list">
          
          <div class="accordion_item" v-if="product.description">
             <button class="accordion_header active" style="cursor: default;">
                商品詳細介紹
             </button>
             <div class="accordion_content" style="max-height: none; padding-bottom: 20px;">
                <p>{{ product.description }}</p>
             </div>
          </div>

          <div class="accordion_item">
            <button 
              class="accordion_header" 
              :class="{ active: accordionStates.important }"
              @click="toggleAccordion('important')"
            >
              重要事項說明
              <i class="fas fa-chevron-down"></i>
            </button>
            <div class="accordion_content" :style="{ maxHeight: accordionStates.important ? '500px' : '0' }">
              <p>本商品為預購商品，預計於產季開始依訂單順序出貨。因農產品受天氣影響，實際出貨日期可能會有所調整，敬請見諒。</p>
            </div>
          </div>

          <div class="accordion_item">
            <button 
              class="accordion_header" 
              :class="{ active: accordionStates.shipping }"
              @click="toggleAccordion('shipping')"
            >
              配送說明
              <i class="fas fa-chevron-down"></i>
            </button>
            <div class="accordion_content" :style="{ maxHeight: accordionStates.shipping ? '500px' : '0' }">
              <p>全程採用黑貓冷藏宅配，確保新鮮送達。收到後請立即開箱檢查，並放入冰箱冷藏保存。</p>
            </div>
          </div>
        </div>

      </div>
    </div>
    
    <div v-else class="loading_state" style="text-align: center; padding: 50px;">
       <p v-if="pending">正在採摘最新鮮的葡萄資訊...</p>
       <p v-else>找不到該商品資料</p>
    </div>
  </section>
</template>

<style src="@/assets/css/ProductDetail.css" scoped></style>