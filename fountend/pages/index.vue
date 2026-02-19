<script setup>
// Nuxt 會自動引入 components 資料夾的東西，通常不用寫 import

// 告訴 Nuxt 這頁要用 default.vue 版型
definePageMeta({
  layout: 'default'
})
</script>

<template>
  <div class="home-page">
    
    <SaleBanner />
    <IntroSection />
    <NewsSection />
    <ProductSection />
    <SelectionSection />
    <ComparisonSection />
    <DessertSection />
    <MediaSection />
    
    </div>
</template>