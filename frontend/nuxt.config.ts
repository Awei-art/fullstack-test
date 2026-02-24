// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: [
    '~/assets/css/header.css',
    '~/assets/css/footer.css',
  ],

  // 2. 新增這一段：專門用來引入外部資源 (CDN)
  app: {
    head: {
      link: [
        { 
          rel: 'stylesheet', 
          href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css' 
        }
      ]
    }
  },
  // API 設定
  runtimeConfig: {
    // 伺服器端 SSR 用（Docker 容器內部網路）
    apiBase: 'http://backend:8000/api',
    public: {
      // 瀏覽器端用（使用者的本機）
      apiBase: 'http://localhost:8000/api'
    }
  },
})

