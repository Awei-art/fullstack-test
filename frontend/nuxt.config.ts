// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt', // 👈 加上這一行
  ],
  css: [
    '~/assets/css/header.css',
    '~/assets/css/footer.css',
  ],

  // 2. 新增這一段：專門用來引入外部資源 (CDN)
  app: {
    head: {
      title: '田原溫室葡萄',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '嚴選田原溫室葡萄，品質把關，產地直送最新鮮的美味。' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        {
          rel: 'stylesheet',
          href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'
        }
      ]
    }
  },
  // API 設定
  runtimeConfig: {
    public: {
      // 伺服器端 (Docker) 連後端容器
      apiBase: 'http://backend:8000/api',
      // 客戶端 (瀏覽器) 連 localhost
      apiBaseClient: 'http://localhost:8000/api'
    }
  }
})

