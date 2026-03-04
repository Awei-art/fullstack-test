<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
const desserts = [
    {
        img: '/images/dessert01.png',
        sub: '每月收到它的喜悅',
        title: '蔬菜採集課程',
        link: '#'
    },
    {
        img: '/images/dessert02.png',
        sub: '說到北海道的秋季風味！',
        title: '目前供應各種馬鈴薯',
        link: '#'
    },
    {
        img: '/images/dessert03.png',
        sub: '米送到家門口',
        title: '北海道米訂閱原因',
        link: '#'
    }
]

const modules = [Navigation]
</script>

<template>
    <section class="dessert_section">
        <div class="dessert_container">
            <ClientOnly>
                <div class="dessert_carousel_wrap">
                    <button class="dessert_nav dessert_prev" type="button"><i class="fas fa-chevron-left"></i></button>
                    
                    <Swiper
                        class="dessert_carousel"
                        :modules="modules"
                        :loop="desserts.length > 3" 
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
                        <SwiperSlide v-for="(item, index) in desserts" :key="index">
                            <div class="dessert_card">
                                <div class="dessert_img_wrap">
                                    <img :src="item.img" :alt="item.title" class="dessert_img">
                                </div>
                                <div class="dessert_info">
                                    <p class="dessert_sub">{{ item.sub }}</p>
                                    <h3 class="dessert_title">{{ item.title }}</h3>
                                    <NuxtLink :to="item.link" class="btn_dessert_more">了解更多</NuxtLink>
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
