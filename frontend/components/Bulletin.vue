<script setup>
import { ref, onMounted } from 'vue'
const config = useRuntimeConfig()

const newsList = ref([])
const isLoading = ref(true)

const activeIndex = ref(null)

const toggleNews = (index) => {
    if (activeIndex.value === index) {
        activeIndex.value = null
    } else {
        activeIndex.value = index
    }
}

onMounted(async () => {
    fetchBulletins()
})

async function fetchBulletins() {
    try {
        isLoading.value = true
        // 注意：這裡使用不需登入憑證的 API
        const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
        const res = await $fetch(`${apiBase}/bulletins/`)
        
        // 建議首頁只顯示最新 4 筆，避免版面過長
        const limitRes = res.slice(0, 4)
        
        // 將資料對應到組件需要的格式
        newsList.value = limitRes.map(item => {
            const dateObj = new Date(item.created_at)
            const year = dateObj.getFullYear()
            const month = String(dateObj.getMonth() + 1).padStart(2, '0')
            const day = String(dateObj.getDate()).padStart(2, '0')
            return {
                id: item.id,
                date: `${year}.${month}.${day}`,
                title: item.title,
                content: item.content
            }
        })
    } catch (e) {
        console.error('載入公告失敗:', e)
    } finally {
        isLoading.value = false
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
                    <div v-if="isLoading" style="padding: 20px; color: #666;">載入中...</div>
                    <div v-else-if="newsList.length === 0" style="padding: 20px; color: #666;">目前無最新快訊</div>
                    <div 
                        v-else
                        v-for="(item, index) in newsList" 
                        :key="item.id" 
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
                <NuxtLink to="/products" class="promo_btn">
                    <img src="/images/promo_banner_tart.png" alt="草莓與葡萄塔饗宴">
                </NuxtLink>
                <NuxtLink to="/desserts" class="promo_btn">
                    <img src="/images/promo_banner_grid.png" alt="甜點禮物大賞">
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