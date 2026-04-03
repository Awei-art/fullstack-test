<script setup>
import { ref, computed, watchEffect, reactive } from 'vue'

// ==========================================
// 購物車邏輯
// ==========================================
import { useCartStore } from '@/stores/cart'
const cartStore = useCartStore()

const route = useRoute()
const config = useRuntimeConfig()
const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient

// 呼叫後端 API
const { data: dessert, pending } = await useFetch(`/desserts/${route.params.id}/`, {
  baseURL: baseURL
})

// ==========================================
// 圖片處理邏輯
// ==========================================
const galleryImages = computed(() => {
  if (!dessert.value) return []
  const list = []
  const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '')

  // 修正圖片 URL 的通用函式
  const fixUrl = (url) => {
    // Cloudinary 優化：自動壓縮與轉成 WebP
    if (typeof url === 'string' && url.includes('res.cloudinary.com') && url.includes('/image/upload/')) {
        if (!url.includes('f_auto') && !url.includes('q_auto')) {
            url = url.replace('/image/upload/', '/image/upload/f_auto,q_auto/')
        }
    }

    if (url.startsWith('http://backend:8000')) {
      return url.replace('http://backend:8000', clientBaseUrl)
    } else if (url.startsWith('/media/')) {
      return `${clientBaseUrl}${url}`
    }
    return url
  }
  
  // 1. 主圖優先
  if (dessert.value.image) {
    list.push(fixUrl(dessert.value.image))
  }

  // 2. 後台上傳的多張額外圖片
  if (dessert.value.images && dessert.value.images.length > 0) {
    dessert.value.images.forEach(img => {
      if (img.image) {
        list.push(fixUrl(img.image))
      }
    })
  }
  
  if (list.length === 0) list.push('/images/default-grape.png')
  return list
})

const currentImage = ref('')

watchEffect(() => {
  if (galleryImages.value.length > 0) {
    if (!currentImage.value || !galleryImages.value.includes(currentImage.value)) {
      currentImage.value = galleryImages.value[0]
    }
  }
})

const changeImage = (imgSrc) => {
  currentImage.value = imgSrc
}

// ==========================================
// 甜點規格 (由後端傳回的 grades)
// ==========================================
const currentGrade = ref(null)

watchEffect(() => {
  if (dessert.value && dessert.value.grades && dessert.value.grades.length > 0) {
    if (!currentGrade.value) {
      currentGrade.value = dessert.value.grades[0]
    }
  }
})

const selectGrade = (grade) => {
  currentGrade.value = grade
  quantity.value = 1
}

// ==========================================
// 計算最終顯示的價格與庫存
// ==========================================
const displayPrice = computed(() => {
  if (currentGrade.value) {
    return currentGrade.value.price
  }
  return dessert.value?.price || 0
})

const displayStock = computed(() => {
  if (currentGrade.value) {
    return currentGrade.value.stock
  }
  return dessert.value?.stock || 0
})

const isSoldOut = computed(() => {
  if (!dessert.value || !dessert.value.is_active) return true
  
  // 1. 如果有規格（6顆/9顆...），就把所有規格的庫存加總
  if (dessert.value.grades && dessert.value.grades.length > 0) {
      const totalGradeStock = dessert.value.grades.reduce((sum, g) => sum + g.stock, 0)
      return totalGradeStock <= 0
  }
  
  // 2. 如果沒有規格（例如單賣1個大福），就看原本的欄位
  return dessert.value.stock <= 0
})

// ==========================================
// 數量
// ==========================================
const quantity = ref(1)

const updateQty = (change) => {
  let val = quantity.value + change
  if (val < 1) val = 1
  if (val > displayStock.value) val = displayStock.value
  quantity.value = val
}

const checkQty = (event) => {
  let val = parseInt(event.target.value)
  if (isNaN(val) || val < 1) val = 1
  if (val > displayStock.value) val = displayStock.value
  quantity.value = val
  event.target.value = val
}

// ==========================================
// 格式化工具
// ==========================================
const formatPrice = (price) => {
  return price?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") || '0'
}

// ==========================================
// 手風琴
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
const addToCart = (skipOpen = false) => {
  if (isSoldOut.value || displayStock.value === 0) return

  const cartItem = {
    itemType: 'dessert',
    id: dessert.value.id,
    productId: dessert.value.id,
    name: dessert.value.name,
    image: galleryImages.value[0], 
    price: displayPrice.value,
    quantity: quantity.value,
    gradeId: currentGrade.value ? currentGrade.value.id : null,
    gradeName: currentGrade.value ? currentGrade.value.name : null,
    varieties: [],
    maxStock: displayStock.value 
  }

  const success = cartStore.addToCart(cartItem, skipOpen)

  if (success && !skipOpen) {
    cartStore.openMiniCart()
  }
  
  return success
}

const buyNow = () => {
    cartStore.closeMiniCart()
    const added = addToCart(true)
    if (added) {
      navigateTo('/cart')
    } else {
      navigateTo('/cart') 
    }
}

// 麵包屑導覽列
const breadcrumbs = computed(() => {
  if (!dessert.value) return []
  return [
    { name: '首頁', path: '/' },
    { name: '甜點專區', path: '/desserts' },
    { name: dessert.value.name }
  ]
})

</script>

<template>
  <section class="product_detail_section">
    <!-- 麵包屑導覽列 -->
    <AppBreadcrumb v-if="dessert" :items="breadcrumbs" />

    <div class="product_detail_container" v-if="dessert">
      
      <div class="detail_gallery">
        <div class="main_image_wrap">
          <img :src="currentImage" :alt="dessert.name" class="main_image" id="mainImage">
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
        <span class="brand_tag">TIANYUAN FRUIT DESSERT</span>
        
        <h1 class="detail_product_title">{{ dessert.name }}</h1>
        <hr class="product_title_divider">

        <div class="detail_price">
          NT${{ formatPrice(displayPrice) }} <span>(含稅)</span>
        </div>

        <div class="option_group" v-if="dessert.grades && dessert.grades.length > 0">
          <span class="option_label">規格選擇</span>
          <div class="grade_row">
            <div 
              v-for="grade in dessert.grades" 
              :key="grade.id"
              class="grade_btn" 
              :class="{ active: currentGrade?.id === grade.id }"
              @click="selectGrade(grade)"
            >
              {{ grade.name }}
            </div>
          </div>
        </div>

        <div class="option_group">
          <span class="option_label">運送方式</span>
          <button class="selected_shipping">
            黑貓冷凍宅配 (運費另計)
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
            :disabled="isSoldOut || displayStock === 0" 
            :class="{ 'btn-disabled': isSoldOut || displayStock === 0}"
            >   
            <template v-if="isSoldOut || displayStock === 0">已售完</template>
            <template v-else>加入購物車</template>
            </button>
          <button 
            class="buy_now_btn" 
            @click="buyNow"
            :disabled="isSoldOut || displayStock === 0"
            :class="{ 'btn-disabled': isSoldOut || displayStock === 0}"
          >
            立即購買
          </button>
        </div>

        <div class="accordion_list">
          
          <div class="accordion_item" v-if="dessert.description">
             <button class="accordion_header active" style="cursor: default;">
                商品詳細介紹
             </button>
             <div class="accordion_content" style="max-height: none; padding-bottom: 20px;">
                <p>{{ dessert.description }}</p>
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
               <p>本商品為接單手工製作，預計將於訂單成立後的 3 ~ 7 個工作天內為您出貨。如有特殊需求，請於訂單備註留言。</p>
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
              <p>全程採用黑貓冷藏宅配，確保新鮮送達。收到後請立即開箱檢查，並放入冰箱冷藏保存，未食用完畢請於 3 天內食用完畢以確保最佳風味。</p>
            </div>
          </div>
        </div>

      </div>
    </div>
    
    <div v-else class="loading_state" style="text-align: center; padding: 50px;">
       <p v-if="pending">正在為您準備甜點資訊...</p>
       <p v-else>找不到該甜點資料</p>
    </div>
  </section>
</template>

<style src="@/assets/css/ProductDetail.css" scoped></style>
