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

### 頁面路由（Pages）

| 路徑 | 說明 |
|------|------|
| `/` | 首頁 |
| `/login` | 登入頁 |
| `/register` | 註冊頁 |
| `/products` | 商品列表 |
| `/products/:id` | 商品詳情 |
| `/cart` | 購物車 |
| `/checkout` | 結帳頁 |
| `/checkout/success` | 結帳成功 |
| `/news` | 最新消息列表 |
| `/news/:id` | 消息詳情 |
| `/about` | 關於田原（靜態） |
| `/varieties` | 品種介紹 |
| `/faq` | 常見問題 |
| `/member` | 會員中心 |
| `/member/profile` | 會員資料 |
| `/member/password` | 修改密碼 |
| `/member/address` | 地址管理 |
| `/member/orders` | 訂單管理 |
| `/member/coupons` | 我的優惠券 |

## 新增元件的標準流程

### Step 1: 建立 CSS 檔案

```css
/* frontend/assets/css/MyComponent.css */
.my_component {
    /* 樣式 */
}
```

### Step 2: 建立 Vue 元件

```vue
<!-- frontend/components/MyComponent.vue -->
<script setup>
// Nuxt 會自動引入 components 資料夾的元件
const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

const { data } = await useFetch('/endpoint/', {
    baseURL: getApiBase(),
    default: () => []
})
</script>

<template>
  <section class="my_component">
    <!-- 模板內容 -->
  </section>
</template>

<style src="@/assets/css/MyComponent.css" scoped></style>
```

### Step 3: 在頁面中使用

```vue
<!-- frontend/pages/my-page.vue -->
<script setup>
definePageMeta({ layout: 'default' })
</script>

<template>
  <div>
    <MyComponent />
  </div>
</template>
```

## CSS 規範

### 檔案組織
- **全域 CSS**：在 `nuxt.config.ts` 的 `css` 陣列中引入（`header.css` 和 `footer.css`）
- **元件 CSS**：使用 `<style src="@/assets/css/XXX.css" scoped></style>` 引入（推薦方式）
- **頁面內嵌**：小型頁面可直接寫 `<style scoped>` 在 `.vue` 檔案內

### 命名規範
- CSS 檔案名稱：與元件同名（PascalCase），如 `ProductSection.css`
- CSS class 名稱：**使用底線分隔**（如 `.news_item_title`），本專案統一此風格
- 頁面級 CSS 以頁面名稱為前綴（如 `.about_hero`、`.news_page`、`.variety_card`）

### 設計風格統一
```css
/* 品牌色系 */
--brown: #5d4037;         /* 標題/深色文字 */
--gold: #dcb15c;          /* 金色強調/按鈕/標籤 */
--beige-bg: #fdfbf7;      /* 米白背景 */
--brown-light: #8d6e63;   /* 次要文字 */
--brown-lighter: #bcaaa4; /* 輔助文字 */
--border-beige: #e0d6cc;  /* 邊線 */

/* 通用字體 */
font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;

/* 英文標題字體 */
font-family: 'Cinzel', serif;
```

### Hero 橫幅統一規範
各頁面（About、FAQ、Varieties、News）使用相同的 Hero 橫幅：
- 電腦版高度：`420px`
- 手機版高度：`280px`
- 遮罩：`linear-gradient(135deg, rgba(93,64,55,0.55), rgba(74,20,140,0.35))`
- 標題：42px / 手機 28px，白色，letter-spacing 0.15em

## API 連線

### 設定（雙模式）
```typescript
// nuxt.config.ts
runtimeConfig: {
  public: {
    apiBase: 'http://backend:8000/api',         // SSR 用（容器內互連）
    apiBaseClient: 'http://localhost:8000/api'   // 客戶端用（瀏覽器直連）
  }
}
```

### 使用方式（推薦）
```vue
<script setup>
const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

// 方式 1: useFetch + baseURL（推薦，支援 SSR）
const { data } = await useFetch('/products/', {
    baseURL: getApiBase(),
    default: () => []
})

// 方式 2: $fetch（純客戶端操作，如提交表單）
const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
const res = await $fetch(`${apiBase}/orders/`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
})
</script>
```

### 圖片路徑處理
後端回傳的圖片 URL 可能是 `http://backend:8000/media/...`，客戶端無法存取。需要轉換：
```javascript
const getImageUrl = (url) => {
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
```

## 第三方套件

### Swiper.js（輪播）
- 已安裝：`swiper@12.1.0`
- 引入方式：`import 'swiper/css'`

### Font Awesome（圖示）
- 透過 CDN 引入（在 nuxt.config.ts 的 app.head.link 中）
- 使用方式：`<i class="fas fa-thumbtack"></i>`

## 重要注意事項
1. Nuxt 會**自動引入** `components/` 資料夾中的元件，不需要手動 import
2. 頁面需要在 `<script setup>` 中用 `definePageMeta({ layout: 'default' })` 指定版型
3. 圖片放在 `public/images/` 下面，引用路徑為 `/images/xxx.png`
4. 修改前端程式碼後需要重啟容器：`docker compose restart frontend`
5. 靜態頁面（如 About）可直接在 `.vue` 中寫內容，不需要 API
6. 動態頁面（如 News、Varieties）從後端 API 取資料，後台可管理
