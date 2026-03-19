<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, EffectFade } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-fade';
import { useRuntimeConfig } from '#app'

const config = useRuntimeConfig()
const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient
const modules = [Autoplay, EffectFade];

// 從後端拉取上架中的輪播圖
const { data: banners, pending } = await useFetch('/banners/', {
    baseURL: baseURL,
    key: 'home-banners',
    default: () => []
})

// 處理圖片路徑 (解決 SSR 與上線部署後的路徑問題，包含 Cloudinary 加速)
const getImageUrl = (url) => {
    if (!url) return '';
    
    // Cloudinary 優化：自動壓縮與轉成 WebP
    if (typeof url === 'string' && url.includes('res.cloudinary.com') && url.includes('/image/upload/')) {
        if (!url.includes('f_auto') && !url.includes('q_auto')) {
            url = url.replace('/image/upload/', '/image/upload/f_auto,q_auto/');
        }
    }

    const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '');
    if (url.startsWith('http://backend:8000')) {
        return url.replace('http://backend:8000', clientBaseUrl);
    }
    if (url.startsWith('/media/')) {
        return `${clientBaseUrl}${url}`;
    }
    return url;
}

// 如果後端沒有任何資料，就給原本預設的陣列做 Fallback
const displayBanners = computed(() => {
    if (banners.value && banners.value.length > 0) {
        return banners.value
    }
    // 預設資料
    return [
        { id: 'default-1', image: '/images/grape01.png', title: '極致美感，濃郁香甜。', subtitle: '在群山環繞的豐饒大地上，\n沐浴著充足的陽光，\n孕育出美麗的田原葡萄。\n日夜溫差累積的甜度，\n令人驚豔的濃郁風味！\n每一顆都如此美麗，如此甘甜。\n這就是，田原溫室葡萄。' },
        { id: 'default-2', image: '/images/grape02.png', title: '品質嚴選，產地直達。', subtitle: '從溫室直接採摘，\n低溫冷藏運輸，\n到您手中依然鮮甜！' },
        { id: 'default-3', image: '/images/grape03.png', title: '天然美味，安心無毒。', subtitle: '嚴格控管每一道程序，\n保證讓您吃得安心！' },
    ]
})

// 追蹤目前的幻燈片索引
const activeIndex = ref(0)
const onSlideChange = (swiper) => {
    activeIndex.value = swiper.realIndex || 0
}

const activeBanner = computed(() => {
    if (displayBanners.value && displayBanners.value.length > 0) {
        return displayBanners.value[activeIndex.value] || displayBanners.value[0]
    }
    return {}
})

// 動態處理大標題 (將文字切成陣列以做成波浪特效)
const titleChars = computed(() => {
    const text = activeBanner.value.title || '極致美感，濃郁香甜。'
    return text.split('')
})

// 動態處理副標題/內文 (依據換行符號切段)
const subtitleLines = computed(() => {
    const text = activeBanner.value.subtitle || ''
    return text.split('\n')
})
</script>

<template>
    <section class="intro_section">
        <div class="intro_container">
            <div class="intro_content">
                <!-- 覆蓋在圖片上的標題 -->
                <div class="intro_hero_text">
                    <p class="intro_subtitle">FROM TIANYUAN GREENHOUSE</p>
                    <h2 class="intro_title">
                        <span v-for="(char, idx) in titleChars" :key="idx" :style="{ '--i': idx + 1 }">
                            {{ char }}
                        </span>
                    </h2>
                </div>

                <!-- 圖片下方的描述文字 -->
                <div class="intro_desc_body intro_desc desktop_split">
                    <p v-for="(line, idx) in subtitleLines" :key="idx">{{ line }}</p>
                </div>
            </div>
            
            <div class="intro_image">
                <div v-if="pending" class="text-center py-5">
                    載入中...
                </div>
                <Swiper v-else
                    :modules="modules"
                    :slides-per-view="1"
                    :loop="true"
                    :effect="'fade'"
                    :autoplay="{
                        delay: 4000,
                        disableOnInteraction: false,
                    }"
                    @slideChange="onSlideChange"
                    class="intro_slider"
                >
                    <SwiperSlide v-for="(banner, index) in displayBanners" :key="banner.id || index">
                        <NuxtLink v-if="banner.link_url" :to="banner.link_url" class="banner_link">
                            <img :src="getImageUrl(banner.image)" :alt="banner.title || '田原葡萄'" class="intro_main_img">
                        </NuxtLink>
                        <img v-else :src="getImageUrl(banner.image)" :alt="banner.title || '田原葡萄'" class="intro_main_img">
                    </SwiperSlide>
                </Swiper>
            </div>
        </div>
    </section>
</template>

<style scoped>
/* 文字波浪動畫 */
.intro_title span {
    display: inline-block;
    animation: wave 2s infinite ease-in-out;
    animation-delay: calc(0.1s * var(--i));
}

@keyframes wave {
    0%, 40%, 100% {
        transform: translateY(0);
        color: inherit;
    }
    20% {
        transform: translateY(-8px);
        color: #8b6aff; 
    }
}

.banner_link {
    display: block;
    width: 100%;
    height: 100%;
    cursor: pointer;
}
</style>

<style src="@/assets/css/IntroSection.css" scoped></style>