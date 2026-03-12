<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation} from 'swiper/modules' // 加了 Autoplay 讓首頁更生動
import 'swiper/css'
import 'swiper/css/navigation'

// 1. 設定後端 API 網址
const config = useRuntimeConfig()
const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient

// 2. 抓取資料
const { data: rawProducts, pending } = await useFetch('/products/', {
    baseURL: baseURL,
    key: 'home-featured-products',
    default: () => []
})

// 3. 過濾資料：使用更完整的庫存邏輯 (比照購物車防呆)
const availableProducts = computed(() => {
    if (!rawProducts.value) return []
    return rawProducts.value.filter(p => {
        let hasStock = false;
        if (p.grades && p.grades.length > 0) {
            hasStock = p.grades.reduce((sum, g) => sum + g.stock, 0) > 0;
        } else {
            hasStock = p.stock > 0;
        }
        if (!hasStock) return false;

        const activeCount = p.varieties ? p.varieties.length : 0;
        const requiredCount = p.mix_limit || 1;
        if (activeCount < requiredCount) return false;

        return true;
    })
})

// 4. 金額格式化 (加逗號)
const formatPrice = (price) => {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// 5. 處理圖片路徑 (解決 SSR 與上線部署後的路徑問題)
const getImageUrl = (url) => {
    if (!url) return null;
    
    // Cloudinary 優化：自動壓縮與轉成 WebP
    if (typeof url === 'string' && url.includes('res.cloudinary.com') && url.includes('/image/upload/')) {
        if (!url.includes('f_auto') && !url.includes('q_auto')) {
            url = url.replace('/image/upload/', '/image/upload/f_auto,q_auto/');
        }
    }

    if (!url) return '/images/default.png'
    
    // 找出目前前端對外呼叫後端的「根網址」(例如: https://api.yourdomain.com 或 http://127.0.0.1:8000)
    const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '')

    if (url.startsWith('http://backend:8000')) {
        return url.replace('http://backend:8000', clientBaseUrl)
    }
    if (url.startsWith('/media/')) {
        return `${clientBaseUrl}${url}`
    }
    return url
}

// Swiper 設定
const modules = [Navigation]
</script>

<template>
    <section class="product_section">
        <div class="product_container">
            <div class="product_title_area">
                <h3>田原精選系列</h3>
                <p>嚴選優質品種，產地直送的新鮮美味</p>
            </div>

            <div v-if="pending" style="text-align: center; padding: 20px;">
                載入中...
            </div>

            <ClientOnly>
                <div v-if="availableProducts.length > 0" class="product_carousel_wrap">
                    <button class="product_nav product_prev" type="button"><i class="fas fa-chevron-left"></i></button>
                    
                    <Swiper
                        class="product_carousel"
                        :modules="modules"
                        :loop="availableProducts.length > 3" 
                        :navigation="{
                            prevEl: '.product_prev',
                            nextEl: '.product_next'
                        }"
                        :breakpoints="{
                            0: { slidesPerView: 1, spaceBetween: 15 },
                            600: { slidesPerView: 2, spaceBetween: 20 },
                            1000: { slidesPerView: 3, spaceBetween: 30 }
                        }"
                    >
                        <SwiperSlide v-for="product in availableProducts" :key="product.id">
                            <div class="product_card">
                                <div class="card_img_wrap">
                                    <img :src="getImageUrl(product.image)" :alt="product.name" class="card_img">
                                </div>
                                <div class="card_content">
                                    <h4 class="card_title">{{ product.name }}</h4>

                                    <p class="card_desc">{{ product.short_description }}</p>
                                    
                                    <div class="card_bottom">
                                        <span class="card_price">
                                            NT$ {{ formatPrice(product.price) }} 
                                            <small>/ 盒</small>
                                        </span>
                                        <NuxtLink :to="`/products/${product.id}`" class="btn_card_action">前往選購</NuxtLink>
                                    </div>
                                </div>
                            </div>
                        </SwiperSlide>
                    </Swiper>

                    <button class="product_nav product_next" type="button"><i class="fas fa-chevron-right"></i></button>
                </div>

                <div v-else style="text-align: center; padding: 20px; color: #666;">
                    目前所有商品熱銷補貨中，敬請期待！
                </div>
            </ClientOnly>
        </div>
    </section>
</template>

<style scoped>
/* Ensure Swiper slide takes full height if needed, though product_card usually handles it */
.swiper-slide {
    height: auto;
    display: flex;
    justify-content: center;
}

/* Ensure product card takes full width inside slide */
.product_card {
    width: 100%;
}

/* Fix for custom nav positioning if needed */
.product_carousel_wrap {
    position: relative;
    display: flex;
    align-items: center;
    gap: 10px; /* Space between nav buttons and swiper if flex layout */
}

/* Override Swiper default pagination if necessary to match design */

</style>

<style src="@/assets/css/ProductSection.css" scoped></style>