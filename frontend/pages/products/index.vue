<script setup>
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

const activeCategory = ref(null)
const activeColor = ref(null)

// 蠟筆風顏色對應表（跟品種介紹頁一致）
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
const getColorCss = (name) => colorMap[name] || '#b39ddb'

// 取得商品分類
const { data: categories } = await useFetch('/products/categories/', {
    baseURL: getApiBase(),
    key: 'product-categories',
    default: () => []
})

// 取得所有商品（用來提取可用顏色）
const { data: allProducts, execute: fetchAllProducts } = await useFetch('/products/', {
    baseURL: getApiBase(),
    key: 'all-products-colors',
    default: () => [],
    query: computed(() => {
        const q = {}
        if (activeCategory.value) q.category = activeCategory.value
        return q
    }),
    watch: false
})

watch(activeCategory, () => {
    fetchAllProducts()
})

// 從當前分類的商品中提取所有品種顏色
const availableColors = computed(() => {
    if (!allProducts.value || !allProducts.value.length) return []
    
    const colors = new Set()
    for (const p of allProducts.value) {
        if (p.varieties && Array.isArray(p.varieties)) {
            for (const v of p.varieties) {
                if (v.color) colors.add(v.color)
            }
        }
    }
    return [...colors]
})

// 判斷目前選擇的是否為「單品種禮盒」
const isSingleVariety = computed(() => {
    if (!activeCategory.value || !categories.value) return false
    const cat = categories.value.find(c => c.id === activeCategory.value)
    return cat && cat.name === '單品種禮盒'
})

const setCategory = (catId) => {
    activeCategory.value = catId
    activeColor.value = null // 切換分類時重置顏色
}

const setColor = (color) => {
    activeColor.value = color
}

// 傳給 ProductSalesSection
provide('activeCategory', activeCategory)
provide('activeColor', activeColor)
</script>

<template>
  <div>

    <!-- Hero 橫幅 -->
    <section class="products_hero">
        <div class="products_hero_overlay"></div>
        <div class="products_hero_content">
            <h1 class="products_hero_title">葡萄禮盒</h1>
            <p class="products_hero_subtitle">嚴選田園溫室栽培，送禮自用兩相宜</p>
        </div>
    </section>

    <!-- 分類 Tab -->
    <div class="products_category_tabs">
        <button
            class="products_tab"
            :class="{ active: !activeCategory }"
            @click="setCategory(null)"
        >
            全部禮盒
        </button>
        <button
            v-for="cat in categories"
            :key="cat.id"
            class="products_tab"
            :class="{ active: activeCategory === cat.id }"
            @click="setCategory(cat.id)"
        >
            {{ cat.name }}
        </button>
    </div>

    <!-- 顏色 Sub-filter（選了「單品種禮盒」才顯示） -->
    <div v-if="isSingleVariety && availableColors.length > 1" class="products_color_filter">
        <button
            class="color_chip"
            :class="{ active: !activeColor }"
            @click="setColor(null)"
        >
            <span class="color_grape all_grape"></span>
            <span>全部</span>
        </button>
        <button
            v-for="color in availableColors"
            :key="color"
            class="color_chip"
            :class="{ active: activeColor === color }"
            @click="setColor(color)"
        >
            <span class="color_grape" :style="{ backgroundColor: getColorCss(color) }"></span>
            <span>{{ color }}</span>
        </button>
    </div>

    <ProductSalesSection />

  </div>
</template>

<style scoped>
.products_hero {
    position: relative;
    height: 420px;
    background: url('https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=1600&h=600&fit=crop') center/cover no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
}

.products_hero_overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(93, 64, 55, 0.55), rgba(74, 20, 140, 0.35));
}

.products_hero_content {
    position: relative;
    z-index: 1;
    text-align: center;
    color: #fff;
}

.products_hero_title {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 0.15em;
    margin-bottom: 14px;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

.products_hero_subtitle {
    font-size: 17px;
    letter-spacing: 0.08em;
    opacity: 0.9;
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

/* 分類 Tab */
.products_category_tabs {
    display: flex;
    justify-content: center;
    gap: 0;
    padding: 40px 0 0;
    border-bottom: 1px solid #e0d6cc;
    background-color: #fdfbf7;
}

.products_tab {
    background: transparent;
    border: none;
    padding: 14px 30px;
    font-size: 15px;
    color: #8d6e63;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
    letter-spacing: 0.05em;
}

.products_tab::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: transparent;
    transition: background-color 0.3s ease;
}

.products_tab:hover {
    color: #5d4037;
}

.products_tab.active {
    color: #6f2da8;
    font-weight: 700;
}

.products_tab.active::after {
    background-color: #6f2da8;
}

/* 顏色篩選列 */
.products_color_filter {
    display: flex;
    justify-content: center;
    gap: 12px;
    padding: 20px 20px;
    background-color: #fdfbf7;
    flex-wrap: wrap;
}

.color_chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border: 1.5px solid #e0d6cc;
    border-radius: 30px;
    background: #fff;
    font-size: 13px;
    color: #8d6e63;
    cursor: pointer;
    transition: all 0.25s ease;
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

.color_chip:hover {
    border-color: #6f2da8;
    color: #5d4037;
}

.color_chip.active {
    border-color: #6f2da8;
    background: rgba(111, 45, 168, 0.06);
    color: #6f2da8;
    font-weight: 600;
}

/* 葡萄顆粒圖示 */
.color_grape {
    position: relative;
    width: 14px;
    height: 16px;
    border-radius: 50% 50% 50% 50% / 45% 45% 55% 55%;
    box-shadow:
        inset -1px -2px 3px rgba(0, 0, 0, 0.25),
        inset 1px 1px 2px rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
}

.color_grape::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 4px;
    height: 4px;
    background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, transparent 70%);
    border-radius: 50%;
}

.all_grape {
    background: conic-gradient(#5c4a6e 0% 33%, #ea344f 33% 66%, #9dc94f 66% 100%);
}

@media (max-width: 900px) {
    .products_hero {
        height: 280px;
    }

    .products_hero_title {
        font-size: 28px;
    }

    .products_hero_subtitle {
        font-size: 14px;
    }

    .products_category_tabs {
        padding: 25px 0 0;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        justify-content: flex-start;
    }

    .products_tab {
        white-space: nowrap;
        padding: 10px 20px;
        font-size: 14px;
    }

    .products_color_filter {
        gap: 8px;
        padding: 15px 15px;
    }

    .color_chip {
        padding: 5px 12px;
        font-size: 12px;
    }
}
</style>