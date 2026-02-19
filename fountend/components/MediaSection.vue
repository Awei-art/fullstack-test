<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay } from 'swiper/modules';
import 'swiper/css';

const mediaList = [
    {
        type: 'video',
        url: 'https://www.youtube.com/embed/TOtOgUNrIO8?rel=0',
        img: '/images/S__41623562_0.jpg',
        alt: '葡萄園影片'
    },
    {
        type: 'image',
        url: null,
        img: '/images/grape01.png',
        alt: '特級葡萄'
    },
    {
        type: 'image',
        url: null,
        img: '/images/grape02.png',
        alt: '溫室栽培'
    },
    {
        type: 'image',
        url: null,
        img: '/images/grape03.png',
        alt: '甜度保證'
    },
    {
        type: 'image',
        url: null,
        img: '/images/grape04.png',
        alt: '新鮮採摘'
    },
    {
        type: 'image',
        url: null,
        img: '/images/grape07.png',
        alt: '特選葡萄'
    }
]

const modules = [Autoplay];

const handlePopup = (item) => {
    if (item.type === 'video') {
        window.open(item.url, '_blank');
    } else {
        console.log("View image: " + item.img);
    }
}

const handleGameStart = (e) => {
    e.preventDefault();
    alert("開始冒險！ (模擬功能)");
}

const updateClasses = (swiper) => {
    // Clear custom classes first
    const slides = swiper.slides;
    slides.forEach(slide => {
        slide.classList.remove('custom-center');
        const thumbWrap = slide.querySelector('.media_thumb_wrap');
        if (thumbWrap) {
            thumbWrap.classList.remove('nextThumb', 'nnextThumb', 'prevThumb', 'pprevThumb');
        }
    });

    // Get active index (real index calculation handling loop)
    const activeIndex = swiper.activeIndex;
    
    // Add custom-center to active slide
    if (slides[activeIndex]) {
        slides[activeIndex].classList.add('custom-center');
    }

    // Helper to safely add class to relative indices
    const addClassToRelative = (offset, className) => {
        const targetIndex = activeIndex + offset;
        if (slides[targetIndex]) {
            const thumbWrap = slides[targetIndex].querySelector('.media_thumb_wrap');
            if (thumbWrap) thumbWrap.classList.add(className);
        }
    };

    // Add classes to neighbors
    addClassToRelative(1, 'nextThumb');
    addClassToRelative(2, 'nnextThumb');
    addClassToRelative(-1, 'prevThumb');
    addClassToRelative(-2, 'pprevThumb');
}
</script>

<template>
    <div class="multi_wrap">
        <section class="media_wrap">
            <Swiper
                class="media_list_area"
                :modules="modules"
                :loop="true"
                :centeredSlides="true"
                :autoplay="{
                    delay: 5000,
                    disableOnInteraction: false,
                }"
                :speed="800"
                :breakpoints="{
                    0: {
                        slidesPerView: 1.45,
                        spaceBetween: 15
                    },
                    768: {
                        slidesPerView: 2.0,
                        spaceBetween: 40
                    },
                    1000: {
                        slidesPerView: 2.5,
                        spaceBetween: 50
                    },
                    1400: {
                        slidesPerView: 3,
                        spaceBetween: 100
                    }
                }"
                @slideChange="updateClasses"
                @init="updateClasses"
            >
                <SwiperSlide v-for="(item, index) in mediaList" :key="index">
                    <div class="media_thumb_wrap">
                        <button 
                            type="button" 
                            class="media_thumb js-viewPop" 
                            :class="item.type === 'video' ? 'view_movie' : 'view_img'"
                            @click="handlePopup(item)"
                        >
                            <img :src="item.img" :alt="item.alt" class="media_thumb_large">
                            <img :src="item.img" :alt="item.alt" class="media_thumb_small">
                        </button>
                    </div>
                </SwiperSlide>
            </Swiper>
        </section>

        <section class="download_wrap">
            <div class="download_subject">
                <h2 class="section_title bold">踏上你的美味之旅</h2>
            </div>
            <div class="downalod_btn_wrap">
                <a href="#" class="btn_deepyellow" @click="handleGameStart">立即訂購</a>
            </div>
        </section>
    </div>
</template>

<style src="@/assets/css/MediaSection.css" scoped></style>
