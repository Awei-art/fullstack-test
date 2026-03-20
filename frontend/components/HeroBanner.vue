<script setup>
const { getByKey } = await useSiteImages()

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    required: false,
    default: ''
  }
})

const heroBg = getByKey('hero_banner', '/images/hero_banner.jpg')
const bgStyle = computed(() => ({
  backgroundImage: `url(${heroBg})`
}))
</script>

<template>
  <section class="hero_banner" :style="bgStyle">
    <div class="hero_overlay"></div>
    <div class="hero_content">
      <h1 class="hero_title">{{ title }}</h1>
      <p class="hero_subtitle" v-if="subtitle">{{ subtitle }}</p>
    </div>
    <!-- 底部的羽化/霧化漸層過渡效果 -->
    <div class="hero_fade_bottom"></div>
  </section>
</template>

<style scoped>
.hero_banner {
  position: relative;
  /* 增加高度顯示更多圖片 */
  height: 480px;
  /* 調整顯示位置往下一點（利用 background-position: center 20%） */
  background: url('../public/images/hero_banner.jpg') center 20% / cover no-repeat;
  background-position: center 20%;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero_overlay {
  position: absolute;
  inset: 0;
  /* 稍微模糊 (blur) 並提升亮度 (brightness) */
  backdrop-filter: blur(4px) brightness(1.15);
  /* 覆蓋一層極淡的白色玻璃濾鏡，讓畫面更明亮 */
  background: rgba(255, 255, 255, 0.1);
}

.hero_content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
}

.hero_fade_bottom {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 120px; /* 控制羽化漸層的高度可以調整 */
  /* 從透明漸變為網站共同的米白背景色 #fdfbf7，創造無縫連接感 */
  background: linear-gradient(to bottom, rgba(253, 251, 247, 0) 0%, rgba(253, 251, 247, 1) 100%);
  z-index: 2;
  pointer-events: none; /* 確保不會影響到滑鼠點擊 */
}

.hero_title {
  font-size: 42px;
  font-weight: 700;
  letter-spacing: 0.15em;
  margin-bottom: 14px;
  /* 將文字陰影加深一點，避免背景變亮後白字看不清楚 */
  text-shadow: 0 3px 15px rgba(0, 0, 0, 0.45);
  font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

.hero_subtitle {
  font-size: 17px;
  letter-spacing: 0.08em;
  opacity: 0.9;
  font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

/* 手機版響應式 */
@media (max-width: 900px) {
  .hero_banner {
    height: 280px;
  }
  .hero_title {
    font-size: 28px;
  }
  .hero_subtitle {
    font-size: 14px;
  }
}
</style>
