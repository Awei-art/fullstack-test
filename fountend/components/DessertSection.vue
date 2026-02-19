<script setup>
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
</script>

<template>
    <section class="dessert_section">
        <div class="dessert_container">
            <div 
                v-for="(item, index) in desserts" 
                :key="index" 
                class="dessert_card"
            >
                <div class="dessert_img_wrap">
                    <img :src="item.img" :alt="item.title" class="dessert_img">
                </div>
                <div class="dessert_info">
                    <p class="dessert_sub">{{ item.sub }}</p>
                    <h3 class="dessert_title">{{ item.title }}</h3>
                    <NuxtLink :to="item.link" class="btn_dessert_more">了解更多</NuxtLink>
                </div>
            </div>
        </div>
    </section>
</template>
<style src="@/assets/css/DessertSection.css" scoped></style>
