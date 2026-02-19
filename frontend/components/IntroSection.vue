<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, EffectFade } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-fade';

const modules = [Autoplay, EffectFade];
</script>

<template>
    <section class="intro_section">
        <div class="intro_container">
            <div class="intro_content">
                <div class="intro_logo_area">
                    <p style="font-size: 12px; color: #aaa; letter-spacing: 2px;">FROM TIANYUAN GREENHOUSE</p>
                </div>

                <div class="intro_text_wrap intro_desc">
                    <h2 class="intro_title">
                        <span style="--i:1">極</span><span style="--i:2">致</span><span style="--i:3">美</span><span
                            style="--i:4">感</span><span style="--i:5">，</span><span style="--i:6">濃</span><span
                            style="--i:7">郁</span><span style="--i:8">香</span><span style="--i:9">甜</span><span
                            style="--i:10">。</span>
                    </h2>
                    <p>在群山環繞的豐饒大地上，</p>
                    <p>沐浴著充足的陽光，</p>
                    <p>孕育出美麗的<strong>田原葡萄</strong>。</p>
                    <p>日夜溫差累積的甜度，</p>
                    <p>令人驚豔的濃郁風味！</p>
                    <p>每一顆都如此美麗，如此甘甜。</p>
                    <p>這就是，田原溫室葡萄。</p>
                </div>
            </div>
            
            <div class="intro_image">
                <Swiper
                    :modules="modules"
                    :slides-per-view="1"
                    :loop="true"
                    :effect="'fade'"
                    :autoplay="{
                        delay: 4000,
                        disableOnInteraction: false,
                    }"
                    class="intro_slider"
                >
                    <SwiperSlide>
                        <img src="/images/grape01.png" alt="田原葡萄 1" class="intro_main_img">
                    </SwiperSlide>
                    <SwiperSlide>
                        <img src="/images/grape02.png" alt="田原葡萄 2" class="intro_main_img">
                    </SwiperSlide>
                    <SwiperSlide>
                        <img src="/images/grape03.png" alt="田原葡萄 3" class="intro_main_img">
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
</style>

<style src="@/assets/css/IntroSection.css" scoped></style>