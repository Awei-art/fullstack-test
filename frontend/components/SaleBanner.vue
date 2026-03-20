<script setup>
import { computed } from 'vue'

const { getByKey, getTitleByKey, getDescByKey, getLinkByKey } = await useSiteImages()

// 動態背景圖片 (若後台沒設，則用預設值)
const bgImageUrl = computed(() => {
    const url = getByKey('top_sale_banner')
    return url ? `url('${url}')` : "url('/images/sale_banner_bg_tech_grey.svg')"
})

// 動態文字 (預設為 2026現正熱賣中品種: 巨峰葡萄)
const bannerTitle = computed(() => getTitleByKey('top_sale_banner') || "2026現正熱賣中品種:")
const bannerDesc = computed(() => getDescByKey('top_sale_banner') || "巨峰葡萄")
const bannerLink = computed(() => getLinkByKey('top_sale_banner') || "/products")
</script>

<template>
    <div class="sale_event_banner" :style="{ '--bg-url': bgImageUrl }">
        <NuxtLink :to="bannerLink" class="sale_link">
            <p>{{ bannerTitle }}<span class="txt_yellow"> {{ bannerDesc }} </span></p>
            <span class="btn_go">GO</span>
        </NuxtLink>
    </div>
</template>

<style src="@/assets/css/sale_banner.css" scoped></style>