<script setup>
import { ref } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'

const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

// 取得真實甜點資料
const { data: rawDesserts, pending } = await useFetch('/desserts/', {
    baseURL: getApiBase(),
    key: 'home-dessert-list',
    default: () => []
})

// 圖片路徑處理
const getImageUrl = (url) => {
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

const modules = [Navigation]
</script>

<template>
    <section class="dessert_section" v-show="!pending && rawDesserts && rawDesserts.length > 0">
        <div class="dessert_container">
            <ClientOnly>
                <div class="dessert_carousel_wrap">
                    <button class="dessert_nav dessert_prev" type="button"><i class="fas fa-chevron-left"></i></button>
                    
                    <Swiper
                        class="dessert_carousel"
                        :modules="modules"
                        :loop="rawDesserts.length > 3" 
                        :navigation="{
                            prevEl: '.dessert_prev',
                            nextEl: '.dessert_next'
                        }"
                        :breakpoints="{
                            0: { slidesPerView: 1, spaceBetween: 15 },
                            600: { slidesPerView: 2, spaceBetween: 20 },
                            1000: { slidesPerView: 3, spaceBetween: 30 }
                        }"
                    >
                        <SwiperSlide v-for="item in rawDesserts" :key="item.id">
                            <div class="dessert_card">
                                <div class="dessert_img_wrap">
                                    <NuxtLink :to="`/desserts/${item.id}`" style="display:block; width:100%; height:100%;">
                                        <img :src="getImageUrl(item.image) || '/images/default-grape.png'" :alt="item.name" class="dessert_img">
                                    </NuxtLink>
                                </div>
                                <div class="dessert_info">
                                    <h3 class="dessert_title">{{ item.name }}</h3>
                                    
                                    <!-- 價格顯示 -->
                                    <div class="dessert_price_wrap" style="color: #e8627c; font-weight: bold; margin-bottom: 20px; font-size: 1.1rem;">
                                        <small>NT$</small> {{ getDisplayPrice(item) }}<small v-if="hasMultipleGrades(item)" style="font-size: 0.85rem; font-weight: normal; color: #b0707e;"> 起</small>
                                    </div>

                                    <NuxtLink :to="`/desserts/${item.id}`" class="btn_dessert_more">了解更多</NuxtLink>
                                </div>
                            </div>
                        </SwiperSlide>
                    </Swiper>

                    <button class="dessert_nav dessert_next" type="button"><i class="fas fa-chevron-right"></i></button>
                </div>
            </ClientOnly>
        </div>
    </section>
</template>

<style scoped>
.swiper-slide {
    height: auto;
    display: flex;
    justify-content: center;
}
.dessert_card {
    width: 100%;
}
</style>

<style src="@/assets/css/DessertSection.css" scoped></style>
