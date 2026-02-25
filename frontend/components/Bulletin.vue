<script setup>
import { ref } from 'vue'

const newsList = [
    {
        date: '2026.01.27',
        title: '春節期間出貨公告',
        content: '親愛的顧客您好，春節期間（1/28 - 2/2）物流配送可能有所延遲，建議提早下單。2/3起恢復正常出貨，感謝您的支持與配合。'
    },
    {
        date: '2025.12.15',
        title: '新品「妮娜皇后」限量上市',
        content: '來自日本的夢幻品種「妮娜皇后」紅葡萄，帶有濃郁的牛奶糖香氣，甜度極高，即日起開放限量預購，請把握機會！'
    },
    {
        date: '2025.11.01',
        title: '獲得「優良農產品」認證肯定',
        content: '田原葡萄堅持草生栽培與安全用藥，今年再度獲得國家級優良農產品認證，讓您吃得安心又健康。'
    },
    {
        date: '2025.10.10',
        title: '官網會員募集中',
        content: '加入官網會員即贈送$100元購物金，生日當月再享專屬優惠，消費累積點數還可折抵現金！'
    }
]

const activeIndex = ref(null)

const toggleNews = (index) => {
    if (activeIndex.value === index) {
        activeIndex.value = null
    } else {
        activeIndex.value = index
    }
}
</script>

<template>
    <section class="custom_feature_section">
        <div class="custom_container">
            <!-- Left Side: News List -->
            <div class="news_container">
                <div class="news_header">
                    <h3>快訊 <span class="en_title">Bulletin</span></h3>
                </div>
                <div class="news_list">
                    <div 
                        v-for="(item, index) in newsList" 
                        :key="index" 
                        class="news_item" 
                        :class="{ active: activeIndex === index }"
                    >
                        <div class="news_item_header" @click="toggleNews(index)">
                            <span class="news_date">{{ item.date }}</span>
                            <span class="news_title">{{ item.title }}</span>
                            <i class="fas fa-chevron-down news_icon"></i>
                        </div>
                        <div 
                            class="news_item_content"
                            :style="{ maxHeight: activeIndex === index ? '200px' : null }"
                        >
                            <p>{{ item.content }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Side: Promo Stack -->
            <div class="promo_stack">
                <NuxtLink to="#" class="promo_btn">
                    <img src="/images/test001.png" alt="Promo 1">
                </NuxtLink>
                <NuxtLink to="#" class="promo_btn">
                    <img src="/images/test002.png" alt="Promo 2">
                </NuxtLink>
            </div>
        </div>
    </section>
</template>

<style scoped>
/* Icon rotation */
.news_item.active .news_icon {
    transform: rotate(180deg);
}

/* Transition for max-height */
.news_item_content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;
}
</style>

<style src="@/assets/css/Bulletin.css" scoped></style>