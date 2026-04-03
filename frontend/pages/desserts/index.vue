<script setup>
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

// 分類篩選
const activeCategory = ref(null)

// 取得分類
const { data: categories } = await useFetch('/desserts/categories/', {
    baseURL: getApiBase(),
    key: 'dessert-categories',
    default: () => []
})

// 取得甜點列表
const { data: desserts, pending } = await useFetch('/desserts/', {
    baseURL: getApiBase(),
    key: 'dessert-list',
    default: () => [],
    query: computed(() => {
        const q = {}
        if (activeCategory.value) q.category = activeCategory.value
        return q
    }),
    watch: [activeCategory]
})

const setCategory = (catId) => {
    activeCategory.value = catId
}

// 圖片路徑處理
const getImageUrl = (url) => {
    if (!url) return null;
    
    // Cloudinary 優化：自動壓縮與轉成 WebP
    if (typeof url === 'string' && url.includes('res.cloudinary.com') && url.includes('/image/upload/')) {
        if (!url.includes('f_auto') && !url.includes('q_auto')) {
            url = url.replace('/image/upload/', '/image/upload/f_auto,q_auto/');
        }
    }

    if (!url) return null
    const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '')
    if (url.startsWith('http://backend:8000')) {
        return url.replace('http://backend:8000', clientBaseUrl)
    }
    if (url.startsWith('/media/')) {
        return `${clientBaseUrl}${url}`
    }
    return url
}

// 佔位圖
const placeholderImages = [
    'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400&h=400&fit=crop',
]
const getPlaceholder = (i) => placeholderImages[i % placeholderImages.length]

// 口味顏色對應
const flavorColorMap = {
    '草莓': '#e8627c',
    '水蜜桃': '#f4a77a',
    '麝香葡萄': '#a8d5a2',
}
const getFlavorColor = (flavor) => flavorColorMap[flavor] || '#dcb15c'

// 取得顯示價格（有規格就取最低價，沒有就用原價）
const getDisplayPrice = (dessert) => {
    if (dessert.grades && dessert.grades.length > 0) {
        return Math.min(...dessert.grades.map(g => g.price))
    }
    return dessert.price
}

// 是否有多規格（用來決定要不要加「起」字）
const hasMultipleGrades = (dessert) => {
    return dessert.grades && dessert.grades.length > 1
}

// ====== 購物車相關邏輯 ======
import { useCartStore } from '@/stores/cart'
const cartStore = useCartStore()

const checkSoldOut = (dessert) => {
    if (!dessert.is_active) return true
    
    // 如果有設定規格，就看所有規格加起來的庫存
    if (dessert.grades && dessert.grades.length > 0) {
        const totalGradeStock = dessert.grades.reduce((sum, g) => sum + g.stock, 0)
        return totalGradeStock <= 0
    }
    
    // 如果沒有設定規格，就看原本的總庫存
    return dessert.stock <= 0
}

const addToCart = (dessert) => {
    if (checkSoldOut(dessert)) return
    
    // 解決圖片路徑問題
    let safeImage = getImageUrl(dessert.image) || '/images/default-grape.png'
    
    let currentGrade = null
    let displayStock = dessert.stock
    let displayPrice = dessert.price

    // 試著抓取有庫存的預設等級
    if (dessert.grades && dessert.grades.length > 0) {
        currentGrade = dessert.grades.find(g => g.stock > 0) || dessert.grades[0]
        displayStock = currentGrade.stock
        displayPrice = currentGrade.price
    }

    const cartItem = {
        itemType: 'dessert',
        id: dessert.id,
        productId: dessert.id,
        name: dessert.name,
        image: safeImage,
        price: displayPrice,
        quantity: 1,
        gradeId: currentGrade ? currentGrade.id : null,
        gradeName: currentGrade ? currentGrade.name : null,
        varieties: [],
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
    <div class="dessert_page">

        <!-- Hero 橫幅 -->
        <section class="dessert_hero">
            <div class="dessert_hero_overlay"></div>
            <div class="dessert_hero_content">
                <h1 class="dessert_hero_title">甜點專區</h1>
                <p class="dessert_hero_subtitle">以季節鮮果入餡，每一口都是幸福滋味</p>
            </div>
        </section>

        <!-- 分類 Tab -->
        <div class="dessert_category_tabs">
            <button 
                class="dessert_tab" 
                :class="{ active: !activeCategory }"
                @click="setCategory(null)"
            >
                全部甜點
            </button>
            <button 
                v-for="cat in categories" 
                :key="cat.id"
                class="dessert_tab" 
                :class="{ active: activeCategory === cat.id }"
                @click="setCategory(cat.id)"
            >
                {{ cat.name }}
            </button>
        </div>

        <!-- 載入中 -->
        <div v-if="pending" class="dessert_loading">
            <i class="fas fa-spinner fa-spin"></i> 載入中...
        </div>

        <!-- 甜點列表 -->
        <section v-else-if="desserts.length > 0" class="dessert_section">
            <div class="dessert_container">
                <div class="dessert_grid">
                    <div v-for="(d, i) in desserts" :key="d.id" class="dessert_card">
                        <div class="dessert_card_img_wrap">
                            <NuxtLink :to="`/desserts/${d.id}`" style="display: block; width: 100%; height: 100%;">
                                <img 
                                    :src="getImageUrl(d.image) || getPlaceholder(i)" 
                                    :alt="d.name" 
                                    class="dessert_card_img"
                                    loading="lazy"
                                >
                            </NuxtLink>
                            <span class="dessert_card_flavor_badge" :style="{ backgroundColor: getFlavorColor(d.flavor) }">
                                {{ d.flavor }}
                            </span>
                        </div>
                        <div class="dessert_card_body">
                            <div class="dessert_card_header">
                                <h3 class="dessert_card_name">{{ d.name }}</h3>
                                <span class="dessert_card_price"><small>NT$</small> {{ getDisplayPrice(d) }}<small v-if="hasMultipleGrades(d)" class="price_suffix"> 起</small></span>
                            </div>
                            
                            <div class="dessert_card_footer">
                              <NuxtLink :to="`/desserts/${d.id}`" class="btn_view_dessert">商品詳情</NuxtLink>
                              <button 
                                class="btn_add_cart" 
                                :disabled="checkSoldOut(d)"
                                @click.prevent="addToCart(d)"
                              >
                                <i class="fas fa-cart-plus"></i> 
                              </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 無資料 -->
        <div v-else class="dessert_empty">
            <i class="fas fa-cookie-bite"></i>
            <p>目前暫無甜點上架</p>
        </div>

    </div>
</template>

<style src="@/assets/css/DessertPage.css" scoped></style>
