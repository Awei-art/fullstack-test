<script setup>
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

const { data: varieties, pending } = await useFetch('/varieties/', {
    baseURL: getApiBase(),
    key: 'variety-list',
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

// 佔位圖（沒有上傳圖片時使用）
const placeholderImages = [
    'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1596451190630-186aff535bf2?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=600&h=400&fit=crop',
]
const getPlaceholder = (index) => placeholderImages[index % placeholderImages.length]

// 目前顯示模式
const viewMode = ref('grid') // 'grid' | 'detail'
</script>

<template>
    <div class="variety_page">

        <!-- Hero 橫幅 -->
        <section class="variety_hero">
            <div class="variety_hero_overlay"></div>
            <div class="variety_hero_content">
                <h1 class="variety_hero_title">品種介紹</h1>
                <p class="variety_hero_subtitle">每一顆葡萄，都有獨特的風味故事</p>
            </div>
        </section>

        <!-- 切換模式按鈕 -->
        <div class="variety_view_switcher">
            <button :class="{ active: viewMode === 'grid' }" @click="viewMode = 'grid'">
                <i class="fas fa-th-large"></i> 卡片瀏覽
            </button>
            <button :class="{ active: viewMode === 'detail' }" @click="viewMode = 'detail'">
                <i class="fas fa-list"></i> 詳細介紹
            </button>
        </div>

        <!-- 載入中 -->
        <div v-if="pending" class="variety_loading">
            <i class="fas fa-spinner fa-spin"></i> 載入中...
        </div>

        <template v-else-if="varieties.length > 0">

            <!-- ====== 方案 A：卡片格線 ====== -->
            <section v-if="viewMode === 'grid'" class="variety_section variety_grid_section">
                <div class="variety_container">
                    <div class="variety_grid">
                        <div v-for="(v, i) in varieties" :key="v.id" class="variety_card">
                            <div class="variety_card_img_wrap">
                                <img :src="getImageUrl(v.image) || getPlaceholder(i)" :alt="v.name" class="variety_card_img">
                                <span v-if="v.season" class="variety_card_season">{{ v.season }}</span>
                            </div>
                            <div class="variety_card_body">
                                <div class="variety_card_tags">
                                    <span class="variety_card_color" :style="{ backgroundColor: v.color || '#b39ddb' }"></span>
                                    <span v-if="v.origin" class="variety_card_origin">{{ v.origin }}</span>
                                </div>
                                <h3 class="variety_card_name">{{ v.name }}</h3>
                                <p v-if="v.flavor" class="variety_card_flavor">{{ v.flavor }}</p>
                                <p v-if="v.description" class="variety_card_desc">{{ v.description }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ====== 方案 B：左右交錯詳細介紹 ====== -->
            <section v-else class="variety_section variety_detail_section">
                <div class="variety_container">
                    <div 
                        v-for="(v, i) in varieties" 
                        :key="v.id" 
                        class="variety_detail_row" 
                        :class="{ reverse: i % 2 !== 0 }"
                    >
                        <div class="variety_detail_img_col">
                            <div class="variety_detail_img_wrap">
                                <img :src="getImageUrl(v.image) || getPlaceholder(i)" :alt="v.name" class="variety_detail_img">
                            </div>
                        </div>
                        <div class="variety_detail_text_col">
                            <span class="variety_detail_index">{{ String(i + 1).padStart(2, '0') }}</span>
                            <h3 class="variety_detail_name">{{ v.name }}</h3>
                            <div class="variety_detail_info">
                                <span v-if="v.origin"><i class="fas fa-map-marker-alt"></i> {{ v.origin }}</span>
                                <span v-if="v.season"><i class="fas fa-calendar-alt"></i> {{ v.season }}</span>
                                <span v-if="v.color"><i class="fas fa-palette"></i> {{ v.color }}</span>
                            </div>
                            <p v-if="v.flavor" class="variety_detail_flavor">「{{ v.flavor }}」</p>
                            <p v-if="v.description" class="variety_detail_desc">{{ v.description }}</p>
                        </div>
                    </div>
                </div>
            </section>

        </template>

        <!-- 無資料 -->
        <div v-else class="variety_empty">
            <i class="fas fa-seedling"></i>
            <p>目前暫無品種資料</p>
        </div>

    </div>
</template>

<style src="@/assets/css/VarietyPage.css" scoped></style>
