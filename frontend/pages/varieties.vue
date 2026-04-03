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

// 佔位圖（沒有上傳圖片時使用）
const placeholderImages = [
    'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1596451190630-186aff535bf2?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=600&h=400&fit=crop',
]
const getPlaceholder = (index) => placeholderImages[index % placeholderImages.length]

// 中文顏色名稱 → 蠟筆風 CSS 色碼對應表
const colorMap = {
    '紫黑色': '#5c4a6e',
    '紫色': '#9b7bb8',
    '深紫色': '#7b5ea0',
    '紅寶石色': '#d4726a',
    '紅色': '#ea344f',
    '深紅色': '#b85c5c',
    '玫瑰紅': '#e8879b',
    '翠綠色': '#8ec89a',
    '綠色': '#9dc94f',
    '黃綠色': '#c8d47a',
    '金黃色': '#edc96a',
    '黑色': '#4a4a52',
    '粉紅色': '#f0a8b8',
    '白色': '#ede8d0',
}

const getColorCss = (colorName) => {
    if (!colorName) return '#b39ddb'
    return colorMap[colorName] || '#b39ddb'
}


</script>

<template>
    <div class="variety_page">

<!-- Hero 橫幅 -->
        <HeroBanner title="品種介紹" subtitle="每一顆葡萄，都有獨特的風味故事" />


        <!-- 載入中 -->
        <div v-if="pending" class="variety_loading">
            <i class="fas fa-spinner fa-spin"></i> 載入中...
        </div>

        <template v-else-if="varieties.length > 0">

            <!-- ====== 卡片格線 ====== -->
            <section class="variety_section variety_grid_section">
                <div class="variety_container">
                    <div class="variety_grid">
                        <div v-for="(v, i) in varieties" :key="v.id" class="variety_card">
                            
                            <!-- 禮物緞帶裝飾 -->
                            <div class="deco-ribbon">
                                <div class="bow">
                                    <div class="bow-center"></div>
                                </div>
                                <div class="ribbon-body">
                                </div>
                            </div>

                            <!-- 通用的圓形裁切與圖片 -->
                            <div class="variety_card_img_wrap">
                                <img :src="getImageUrl(v.image) || getPlaceholder(i)" :alt="v.name" class="variety_card_img" loading="lazy">
                            </div>

                            <div class="variety_card_body">
                                <h3 class="variety_card_name">{{ v.name }}</h3>
                                <!-- 產地與產季分隔線 -->


                                <p v-if="v.flavor" class="variety_card_flavor">{{ v.flavor }}</p>
                                <p v-if="v.description" class="variety_card_desc">{{ v.description }}</p>
                            </div>
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
