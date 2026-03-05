---
name: 靜態頁面開發規範
description: 如何建立品牌介紹、FAQ 等靜態頁面，包含 Hero 橫幅、左右交錯排版、設計風格統一的規範
---

# 靜態頁面開發規範

## 概述
靜態頁面是指不需要後台動態管理內容的頁面，如「關於田原」、「常見問題 FAQ」等。
這類頁面內容較少變動，直接在 `.vue` 檔案中撰寫 HTML 即可。

## 適用場景判斷

| 情境 | 建議 |
|------|------|
| 品牌故事、公司介紹、團隊介紹 | ✅ 靜態 |
| 常見問題 FAQ | ✅ 靜態 |
| 隱私政策、使用條款 | ✅ 靜態 |
| 最新消息、公告 | ❌ 動態（內容經常變動） |
| 品種介紹（未來會新增品種） | ❌ 動態（用 API） |
| 商品頁面 | ❌ 動態（用 API） |

## 頁面結構模板

### 基本結構
```vue
<script setup>
definePageMeta({ layout: 'default' })
</script>

<template>
    <div class="page_name">
        <!-- Hero 橫幅 -->
        <section class="page_hero">
            <div class="page_hero_overlay"></div>
            <div class="page_hero_content">
                <h1 class="page_hero_title">頁面標題</h1>
                <p class="page_hero_subtitle">副標題描述</p>
            </div>
        </section>

        <!-- 內容區塊 -->
        <section class="page_section">
            <div class="page_container">
                <!-- 內容 -->
            </div>
        </section>
    </div>
</template>

<style src="@/assets/css/PageName.css" scoped></style>
```

## Hero 橫幅統一規範

所有靜態頁面的 Hero 橫幅遵循相同的設計：

```css
.page_hero {
    position: relative;
    height: 420px;                          /* 電腦版 */
    background: url('圖片URL') center/cover no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
}

.page_hero_overlay {
    position: absolute;
    inset: 0;
    /* 棕色→紫色漸層遮罩（品牌統一） */
    background: linear-gradient(135deg, rgba(93,64,55,0.55), rgba(74,20,140,0.35));
}

.page_hero_content {
    position: relative;
    z-index: 1;
    text-align: center;
    color: #fff;
}

.page_hero_title {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

/* 手機版 */
@media (max-width: 900px) {
    .page_hero { height: 280px; }
    .page_hero_title { font-size: 28px; }
}
```

## 常用版型模式

### 模式 1：左右交錯排版
用於品牌故事、農場特色等段落。奇數段左文右圖，偶數段右文左圖。

```html
<div class="about_row">           <!-- 左文右圖 -->
    <div class="about_text_col">文字</div>
    <div class="about_img_col">圖片</div>
</div>

<div class="about_row reverse">   <!-- 右文左圖 -->
    <div class="about_text_col">文字</div>
    <div class="about_img_col">圖片</div>
</div>
```

### 模式 2：帶步驟的時間軸
用於種植流程、製作過程等有順序的內容。

```html
<div class="timeline_item">
    <div class="timeline_img_wrap">圖片</div>
    <div class="timeline_content">
        <span class="timeline_step">01</span>
        <h4>步驟標題</h4>
        <p>步驟說明</p>
    </div>
</div>
```

### 模式 3：特色列表（圖標+文字）
用於農場特色、品牌優勢等。

```html
<div class="feature_item">
    <div class="feature_icon"><i class="fas fa-leaf"></i></div>
    <div>
        <h4>特色標題</h4>
        <p>特色說明</p>
    </div>
</div>
```

## Header 導航連結更新
新增靜態頁面後，記得更新 `AppHeader.vue` 中對應的 `<NuxtLink to="/page-name">` 連結。

## 佔位圖片資源
開發時沒有真實照片可使用 Unsplash 佔位圖：
```
https://images.unsplash.com/photo-XXXX?w=寬度&h=高度&fit=crop
```
上線前替換為真實照片即可。

## 現有靜態頁面
- `/about`：關於田原（Hero + 品牌故事 + 農場特色 + 種植流程 + 農場主人）
- `/faq`：常見問題（Hero + FaqSection 元件）
