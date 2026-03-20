/**
 * 共用 composable：從後端素材庫取得所有圖片，提供 getByKey() 方法用代號取圖
 */
export const useSiteImages = async () => {
    const config = useRuntimeConfig()
    const baseURL = process.server ? config.public.apiBase : config.public.apiBaseClient

    const { data: images } = await useFetch('/site-images/', {
        baseURL,
        key: 'site-images',
        default: () => []
    })

    // 用代號找到對應的圖片網址
    const getByKey = (key, fallback = '') => {
        if (!images.value || images.value.length === 0) return fallback
        const found = images.value.find(img => img.key === key)
        if (!found || !found.image) return fallback

        let url = found.image

        // Cloudinary 優化
        if (typeof url === 'string' && url.includes('res.cloudinary.com') && url.includes('/image/upload/')) {
            if (!url.includes('f_auto') && !url.includes('q_auto')) {
                url = url.replace('/image/upload/', '/image/upload/f_auto,q_auto/')
            }
        }

        // SSR 路徑修正
        const clientBaseUrl = config.public.apiBaseClient.replace(/\/api\/?$/, '')
        if (url.startsWith('http://backend:8000')) {
            return url.replace('http://backend:8000', clientBaseUrl)
        }
        if (url.startsWith('/media/')) {
            return `${clientBaseUrl}${url}`
        }
        return url
    }

    // 用代號取得 alt 文字
    const getAltByKey = (key, fallback = '') => {
        if (!images.value || images.value.length === 0) return fallback
        const found = images.value.find(img => img.key === key)
        return found?.alt_text || fallback
    }

    // 用代號取得標題文字
    const getTitleByKey = (key, fallback = '') => {
        if (!images.value || images.value.length === 0) return fallback
        const found = images.value.find(img => img.key === key)
        return found?.title || fallback
    }

    // 用代號取得介紹文字
    const getDescByKey = (key, fallback = '') => {
        if (!images.value || images.value.length === 0) return fallback
        const found = images.value.find(img => img.key === key)
        return found?.description || fallback
    }

    // 用代號取得跳轉連結
    const getLinkByKey = (key, fallback = '') => {
        if (!images.value || images.value.length === 0) return fallback
        const found = images.value.find(img => img.key === key)
        return found?.link_url || fallback
    }

    return { images, getByKey, getAltByKey, getTitleByKey, getDescByKey, getLinkByKey }
}
