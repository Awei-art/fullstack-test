<script setup>
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

// 分類 Tab 篩選
const activeCategory = ref(null) // null = 全部

// 取得分類列表
const { data: categories } = await useFetch('/news/categories/', {
    baseURL: getApiBase(),
    key: 'news-categories',
    default: () => []
})

// 取得消息列表
const { data: newsList, pending, refresh } = await useFetch('/news/', {
    baseURL: getApiBase(),
    key: 'news-list',
    default: () => [],
    query: computed(() => {
        const q = {}
        if (activeCategory.value) q.category = activeCategory.value
        return q
    }),
    watch: [activeCategory]
})

// 切換分類
const setCategory = (catId) => {
    activeCategory.value = catId
}

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

// 日期格式化
const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return { month, day, year: d.getFullYear() }
}
</script>

<template>
    <section class="news_page">
        <div class="news_page_container">
            <!-- 頁面標題 -->
            <div class="news_page_header">
                <h2 class="news_page_title">最新消息</h2>
                <p class="news_page_subtitle">田原溫室的最新動態與公告資訊</p>
            </div>

            <!-- 分類 Tab -->
            <div class="news_category_tabs">
                <button 
                    class="news_tab" 
                    :class="{ active: !activeCategory }"
                    @click="setCategory(null)"
                >
                    所有訊息
                </button>
                <button 
                    v-for="cat in categories" 
                    :key="cat.id"
                    class="news_tab" 
                    :class="{ active: activeCategory === cat.id }"
                    @click="setCategory(cat.id)"
                >
                    {{ cat.name }}
                </button>
            </div>

            <!-- 載入中 -->
            <div v-if="pending" class="news_loading">
                <i class="fas fa-spinner fa-spin"></i> 載入中...
            </div>

            <!-- 消息列表 -->
            <div v-else-if="newsList.length > 0" class="news_list">
                <NuxtLink 
                    v-for="item in newsList" 
                    :key="item.id" 
                    :to="`/news/${item.id}`" 
                    class="news_item"
                >
                    <!-- 封面圖 -->
                    <div class="news_item_img_wrap">
                        <img 
                            v-if="getImageUrl(item.cover_image)" 
                            :src="getImageUrl(item.cover_image)" 
                            :alt="item.title" 
                            class="news_item_img"
                        >
                        <div v-else class="news_item_img_placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                    </div>
                    
                    <!-- 內容 -->
                    <div class="news_item_body">
                        <div class="news_item_meta">
                            <span v-if="formatDate(item.published_date)" class="news_item_date">
                                <span class="date_month">{{ formatDate(item.published_date).month }}</span>
                                <span class="date_sep">/</span>
                                <span class="date_day">{{ formatDate(item.published_date).day }}</span>
                            </span>
                            <span v-if="item.category_name" class="news_item_category">{{ item.category_name }}</span>
                            <span v-if="item.is_pinned" class="news_item_pinned"><i class="fas fa-thumbtack"></i> 置頂</span>
                        </div>
                        <h3 class="news_item_title">{{ item.title }}</h3>
                        <p v-if="item.summary" class="news_item_summary">{{ item.summary }}</p>
                        <span class="news_item_more">
                            詳細介紹 <i class="fas fa-arrow-right"></i>
                        </span>
                    </div>
                </NuxtLink>
            </div>

            <!-- 無資料 -->
            <div v-else class="news_empty">
                <i class="fas fa-newspaper"></i>
                <p>目前暫無最新消息</p>
            </div>
        </div>
    </section>
</template>

<style src="@/assets/css/NewsPage.css" scoped></style>
