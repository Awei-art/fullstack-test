<script setup>
// 1. 設定後端 API 網址 (開發時通常是 localhost:8000)
const config = useRuntimeConfig()
const API_BASE = 'http://127.0.0.1:8000/api' 

// 2. 使用 Nuxt 的 useFetch 抓取資料
// data 重新命名為 products，並給予預設值 []
const { data: products, pending, error } = await useFetch(`${API_BASE}/products/`, {
  default: () => []
})

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
</script>

<template>
  <section class="grape_sales_section">
    <div class="grape_sales_container">
      <h2 class="grape_sales_title">精選葡萄禮盒</h2>

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
                :src="product.image || '/images/default-grape.png'" 
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
