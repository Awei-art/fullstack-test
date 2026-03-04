<script setup>
// 告訴 Nuxt 這頁要用 default.vue 版型
definePageMeta({
  layout: 'default'
})

//SEO設定
useHead({
  // 1. 瀏覽器分頁標籤 & Google 搜尋標題
  title: '常見問題 FAQ - 田原溫室',
  
  meta: [
    // 2. Google 搜尋下方的灰色小字
    { name: 'description', content: '這裡匯集了關於葡萄保存、運送方式以及訂購相關的常見問題，讓您買得安心，吃得開心。' },

    // --- 👇 新增這些讓 Line/FB 分享更漂亮 👇 ---
    
    // 3. FB/Line 分享卡片的標題
    { property: 'og:title', content: '常見問題 FAQ - 田原溫室' },
    
    // 4. FB/Line 分享卡片的描述
    { property: 'og:description', content: '這裡匯集了關於葡萄保存、運送方式以及訂購相關的常見問題。' },
    
    // 5. ★最重要★ FB/Line 分享時顯示的縮圖 (建議找一張最漂亮的葡萄圖)
    // 注意：這裡必須用「絕對路徑」(也就是要有 https://你的網址...)
    // 本機開發時看不到效果是正常的，上線後就會有圖片了
    { property: 'og:image', content: 'https://www.your-website.com/images/grape01.png' },
    
    // 6. 告訴 FB/Line 這是一張網頁
    { property: 'og:type', content: 'website' }
  ]
})
</script>


<template>
  <div>

    <!-- Hero 橫幅 -->
    <section class="faq_hero">
        <div class="faq_hero_overlay"></div>
        <div class="faq_hero_content">
            <h1 class="faq_hero_title">常見問題 FAQ</h1>
            <p class="faq_hero_subtitle">您的疑問，我們用心解答</p>
        </div>
    </section>

    <FaqSection />

  </div>
</template>


<style scoped>
.faq_hero {
    position: relative;
    height: 420px;
    background: url('https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=1600&h=600&fit=crop') center/cover no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
}

.faq_hero_overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(93, 64, 55, 0.55), rgba(74, 20, 140, 0.35));
}

.faq_hero_content {
    position: relative;
    z-index: 1;
    text-align: center;
    color: #fff;
}

.faq_hero_title {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 0.15em;
    margin-bottom: 14px;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

.faq_hero_subtitle {
    font-size: 17px;
    letter-spacing: 0.08em;
    opacity: 0.9;
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

@media (max-width: 900px) {
    .faq_hero {
        height: 280px;
    }
    .faq_hero_title {
        font-size: 28px;
    }
    .faq_hero_subtitle {
        font-size: 14px;
    }
}
</style>





