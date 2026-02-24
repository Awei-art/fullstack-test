<script setup>
import { ref, computed, watchEffect, reactive } from 'vue'

const route = useRoute()
// 1. 設定後端 API
const config = useRuntimeConfig()
const { data: product, pending } = useFetch(`${config.public.apiBase}/products/${route.params.id}/`, {
  server: false,
  lazy: true,
})

// ==========================================
// 圖片處理邏輯
// ==========================================
const galleryImages = computed(() => {
  if (!product.value) return []
  const list = []
  
  // 1. 封面圖
  if (product.value.image) list.push(product.value.image)
  
  // 2. 相簿圖 (後端回傳的是物件陣列，要取出 image 欄位)
  if (product.value.images && product.value.images.length > 0) {
    product.value.images.forEach(imgObj => {
      list.push(imgObj.image)
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
  // A. 檢查是否已選
  const index = selectedVarieties.value.findIndex(item => item.id === variety.id)

  if (index > -1) {
    // 移除 (永遠允許)
    selectedVarieties.value.splice(index, 1)
  } else {
    // B. 加入前，先讀取後端給的上限 (如果後端沒給，預設為 1)
    const limit = product.value.mix_limit || 1
    
    if (selectedVarieties.value.length >= limit) {
      return 
    }
    
    // 加入陣列
    selectedVarieties.value.push(variety)
  }
}

// 3. 🔥 防呆監聽邏輯改變：確保「已選名單」裡的品種都是活著的
watchEffect(() => {
  // 確認產品存在、是混合禮盒、且有品種列表
  if (product.value?.is_mixed && product.value?.varieties?.length > 0) {
    
    // 取得目前後端回傳「有貨且有效」的所有 ID 列表
    const validIds = product.value.varieties.map(v => v.id)

    // 過濾：只保留那些「ID 還在有效列表內」的品種
    // (如果原本選了 A, B，結果後台把 B 關掉，這裡就會自動把 B 踢除，只剩 A)
    const newSelection = selectedVarieties.value.filter(selected => validIds.includes(selected.id))

    // 如果過濾後的長度跟原本不一樣，代表有品種失效了，更新列表
    if (newSelection.length !== selectedVarieties.value.length) {
      selectedVarieties.value = newSelection
    }

  } else {
    // 如果不是混合禮盒或是沒貨了，清空所有選擇
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
// 購物車按鈕 (暫時功能)
// ==========================================
const addToCart = () => {
    if(!product.value) return
    alert(`已加入購物車：${product.value.name} x ${quantity.value}`)
    // 這裡之後可以串接 Pinia 或 Vuex 購物車狀態
}

</script>

<template>
  <section class="product_detail_section">
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
            <img :src="img" :alt="'Thumb ' + (index + 1)" class="thumb_img">
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
            @click="addToCart" 
            :disabled="isSoldOut || displayStock === 0" 
            :class="{ 'btn-disabled': isSoldOut || displayStock === 0}"
            >   
            {{ (isSoldOut || displayStock === 0) ? '已售完' : '加入購物車' }}
            </button>
          <button 
            v-if="!isSoldOut && displayStock > 0"
            class="buy_now_btn" 
            @click="buyNow"
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