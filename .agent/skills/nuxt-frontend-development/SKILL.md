---
name: Nuxt 前端開發規範
description: 如何在 Nuxt 3 前端新增頁面、元件和樣式的標準流程
---

# Nuxt 3 前端開發規範

## 概述
前端使用 Nuxt 3 + Vue 3 Composition API（`<script setup>`），每個元件有獨立的 CSS 檔案。

## 元件架構

### 版型（Layouts）
- `layouts/default.vue`：預設版型，包含 `<AppHeader />` 和 `<AppFooter />`
- 透過 `<slot />` 渲染頁面內容

### 頁面元件（17 個 Components）

| 元件 | 用途 | CSS 檔案 |
|------|------|---------|
| `AppHeader.vue` | 網站導覽列 | `header.css` |
| `AppFooter.vue` | 網站頁尾 | `footer.css` |
| `SaleBanner.vue` | 優惠橫幅 | `sale_banner.css` |
| `IntroSection.vue` | 商品介紹/輪播 | `IntroSection.css` |
| `NewsSection.vue` | 最新消息 | `NewsSection.css` |
| `ProductSection.vue` | 商品展示輪播 | `ProductSection.css` |
| `SelectionSection.vue` | 品種選擇 | `SelectionSection.css` |
| `ComparisonSection.vue` | 圖片比較 | `ComparisonSection.css` |
| `DessertSection.vue` | 甜點區 | `DessertSection.css` |
| `MediaSection.vue` | 媒體報導 | `MediaSection.css` |
| `ProductDetail.vue` | 商品詳細頁 | `ProductDetail.css` |
| `ProductSalesSection.vue` | 商品銷售區 | `ProductSalesSection.css` |
| `LoginCard.vue` | 登入卡片 | `LoginCard.css` |
| `RegisterCard.vue` | 註冊卡片 | `RegisterCard.css` |
| `CartShop.vue` | 購物車 | - |
| `FaqSection.vue` | 常見問題 | `FaqSection.css` |
| `MemberSidebar.vue` | 會員側欄 | `MemberSidebar.css` |

### 頁面路由（Pages）
- `/` → `index.vue`（首頁）
- `/login` → `login.vue`
- `/register` → `register.vue`
- `/cart` → `cart.vue`
- `/faq` → `faq.vue`
- `/member` → `member.vue`
- `/products/` → `products/index.vue`
- `/products/:id` → `products/[id].vue`

## 新增元件的標準流程

### Step 1: 建立 CSS 檔案

```css
/* frontend/assets/css/MyComponent.css */
.my-component {
    /* 樣式 */
}
```

### Step 2: 建立 Vue 元件

```vue
<!-- frontend/components/MyComponent.vue -->
<script setup>
// Nuxt 會自動引入 components 資料夾的元件，不用手動 import
// 使用 Composition API

// 定義響應式資料
const items = ref([])

// API 呼叫（使用 Nuxt 的 useFetch 或 $fetch）
const { data } = await useFetch('/api/endpoint')
</script>

<template>
  <section class="my-component">
    <!-- 模板內容 -->
  </section>
</template>

<style>
@import '~/assets/css/MyComponent.css';
</style>
```

### Step 3: 在頁面中使用

```vue
<!-- frontend/pages/my-page.vue -->
<script setup>
definePageMeta({
  layout: 'default'
})
</script>

<template>
  <div>
    <MyComponent />
  </div>
</template>
```

## CSS 規範

### 檔案組織
- 全域 CSS：在 `nuxt.config.ts` 的 `css` 陣列中引入（目前有 `header.css` 和 `footer.css`）
- 元件 CSS：在個別 `.vue` 檔案的 `<style>` 中用 `@import` 引入
- 舊版 CSS：`styles/` 資料夾中有舊版的 CSS 檔案（非 Nuxt 版本）

### 命名規範
- CSS 檔案名稱：與元件同名（PascalCase），如 `ProductSection.css`
- CSS class 名稱：使用 kebab-case，如 `.product-section`

## API 連線

### 設定
```typescript
// nuxt.config.ts
runtimeConfig: {
  public: {
    apiBase: 'http://127.0.0.1:8000/api'  // 本機開發
  }
}
```

Docker 環境下會透過環境變數覆蓋：
```
NUXT_PUBLIC_API_BASE=http://backend:8000/api
```

### 使用方式
```vue
<script setup>
const config = useRuntimeConfig()

// 方式 1: useFetch（有 SSR 支援）
const { data: products } = await useFetch(`${config.public.apiBase}/products/`)

// 方式 2: $fetch（純客戶端）
const products = await $fetch(`${config.public.apiBase}/products/`)
</script>
```

## 第三方套件

### Swiper.js（輪播）
- 已安裝：`swiper@12.1.0`
- 使用在：IntroSection、ProductSection、MediaSection
- 引入方式：`import 'swiper/css'`

### Font Awesome（圖示）
- 透過 CDN 引入（在 nuxt.config.ts 的 app.head.link 中）
- 使用方式：`<i class="fa-solid fa-cart-shopping"></i>`

## 重要注意事項
1. Nuxt 會**自動引入** `components/` 資料夾中的元件，不需要手動 import
2. 頁面需要在 `<script setup>` 中用 `definePageMeta({ layout: 'default' })` 指定版型
3. 圖片放在 `public/images/` 下面，引用路徑為 `/images/xxx.png`
4. 修改前端程式碼後需要重建容器：`docker compose up -d --build frontend`
