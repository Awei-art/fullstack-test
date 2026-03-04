<script setup>
definePageMeta({ layout: 'default' })

const route = useRoute()
const config = useRuntimeConfig()
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient

const { data: article, pending } = await useFetch(`/news/${route.params.id}/`, {
    baseURL: getApiBase(),
    key: `news-detail-${route.params.id}`,
    default: () => null
})

// 圖片路徑處理
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

// 日期格式化
const formatFullDate = (dateStr) => {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    return `${d.getFullYear()} 年 ${d.getMonth() + 1} 月 ${d.getDate()} 日`
}
</script>

<template>
    <section class="news_detail_page">
        <div class="news_detail_container">
            <!-- 返回按鈕 -->
            <NuxtLink to="/news" class="news_back_btn">
                <i class="fas fa-arrow-left"></i> 返回消息列表
            </NuxtLink>

            <div v-if="pending" class="news_detail_loading">
                <i class="fas fa-spinner fa-spin"></i> 載入中...
            </div>

            <article v-else-if="article" class="news_article">
                <!-- Meta 資訊 -->
                <div class="news_article_meta">
                    <span v-if="article.category_name" class="news_article_category">{{ article.category_name }}</span>
                    <span class="news_article_date">{{ formatFullDate(article.published_date) }}</span>
                </div>

                <!-- 標題 -->
                <h1 class="news_article_title">{{ article.title }}</h1>

                <!-- 封面圖 -->
                <div v-if="getImageUrl(article.cover_image)" class="news_article_cover_wrap">
                    <img :src="getImageUrl(article.cover_image)" :alt="article.title" class="news_article_cover">
                </div>

                <!-- 詳細內容 -->
                <div class="news_article_content" v-html="article.content.replace(/\n/g, '<br>')">
                </div>
            </article>

            <div v-else class="news_detail_notfound">
                <i class="fas fa-exclamation-triangle"></i>
                <p>找不到該篇消息</p>
                <NuxtLink to="/news" class="news_back_link">返回消息列表</NuxtLink>
            </div>
        </div>
    </section>
</template>

<style scoped>
.news_detail_page {
    padding: 80px 0 60px;
    min-height: 80vh;
    background-color: #fdfbf7;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.08'/%3E%3C/svg%3E");
    background-repeat: repeat;
    font-family: 'NaikaiFont', 'Zen Maru Gothic', 'Noto Sans TC', sans-serif;
}

.news_detail_container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 30px;
}

/* 返回按鈕 */
.news_back_btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #8d6e63;
    font-size: 14px;
    text-decoration: none;
    margin-bottom: 40px;
    padding: 8px 0;
    transition: all 0.3s ease;
    letter-spacing: 0.03em;
}

.news_back_btn:hover {
    color: #dcb15c;
}

.news_back_btn i {
    transition: transform 0.3s ease;
}

.news_back_btn:hover i {
    transform: translateX(-4px);
}

/* Meta */
.news_article_meta {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.news_article_category {
    font-size: 13px;
    color: #8d6e63;
    background: rgba(220, 177, 92, 0.15);
    padding: 4px 14px;
    border-radius: 20px;
    letter-spacing: 0.05em;
}

.news_article_date {
    font-size: 14px;
    color: #bcaaa4;
    font-family: 'Noto Sans TC', sans-serif;
}

/* 標題 */
.news_article_title {
    font-size: 28px;
    color: #5d4037;
    font-weight: 700;
    line-height: 1.5;
    letter-spacing: 0.05em;
    margin-bottom: 35px;
}

/* 封面圖 */
.news_article_cover_wrap {
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 40px;
}

.news_article_cover {
    width: 100%;
    height: auto;
    display: block;
}

/* 內容 */
.news_article_content {
    font-size: 16px;
    color: #444;
    line-height: 2;
    letter-spacing: 0.03em;
}

/* 載入中 */
.news_detail_loading {
    text-align: center;
    padding: 80px 0;
    color: #8d6e63;
    font-size: 16px;
}

/* 找不到 */
.news_detail_notfound {
    text-align: center;
    padding: 80px 0;
    color: #bcaaa4;
}

.news_detail_notfound i {
    font-size: 48px;
    margin-bottom: 20px;
    display: block;
    color: #dcb15c;
}

.news_detail_notfound p {
    font-size: 16px;
    margin-bottom: 20px;
}

.news_back_link {
    display: inline-block;
    padding: 10px 30px;
    border: 1px solid #dcb15c;
    border-radius: 30px;
    color: #dcb15c;
    text-decoration: none;
    font-size: 14px;
    transition: all 0.3s ease;
}

.news_back_link:hover {
    background: #dcb15c;
    color: #fff;
}

/* ===== RWD ===== */
@media (max-width: 900px) {
    .news_detail_page {
        padding: 60px 0 40px;
    }

    .news_article_title {
        font-size: 22px;
    }

    .news_article_content {
        font-size: 15px;
        line-height: 1.9;
    }
}
</style>
