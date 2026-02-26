<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useCartStore } from '@/stores/cart'
import MiniCart from '@/components/MiniCart.vue'

// 取得使用者 Cookie
const userCookie = useCookie('user_info')

const cartStore = useCartStore()
const cartTotalQty = computed(() => cartStore.totalQty)

// 🔥 登出功能
const handleLogout = () => {
    if (confirm('確定要登出嗎？')) {
        userCookie.value = null
        navigateTo('/login') // 回到登入頁
    }
}

const openMiniCart = (e) => {
    e.preventDefault()
    cartStore.openMiniCart()
}

const isMenuOpen = ref(false)
const headerRef = ref(null)

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
    isMenuOpen.value = false
}

const handleClickOutside = (event) => {
    // If menu is open and click is outside the header, close the menu
    if (isMenuOpen.value && headerRef.value && !headerRef.value.contains(event.target)) {
        closeMenu()
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
    <header class="header_wrap grape-theme">
        <div class="header" :class="{ 'mobile-menu-open': isMenuOpen }" ref="headerRef">
            <h1 class="logo">
                <NuxtLink to="/" class="logo_link">
                    <img src="/images/logo_icon.svg" alt="田原葡萄Icon" class="logo_icon">
                    <img src="/images/logo_text.svg" alt="田原溫室葡萄" class="logo_default">
                </NuxtLink>
            </h1>

            <nav>
                <ul class="header_menu_wrap" :style="{ display: isMenuOpen ? 'flex' : '' }">
                    <li class="mobile_menu_logo_item">
                        <NuxtLink to="/">
                            <img src="/images/menu_header.png" alt="田原溫室">
                        </NuxtLink>
                    </li>
                    <li class="node1">
                        <NuxtLink to="#" class="menu_link">
                            <span>最新消息</span>
                        </NuxtLink>
                    </li>
                    <li class="node1">
                        <NuxtLink to="#" class="menu_link">
                            <span>關於田原</span>
                        </NuxtLink>
                    </li>
                    <li class="node1">
                        <NuxtLink to="/products" class="menu_link">
                            <span>葡萄商店</span>
                        </NuxtLink>
                    </li>
                    <li class="node1">
                        <NuxtLink to="#" class="menu_link">
                            <span>品種介紹</span>
                        </NuxtLink>
                    </li>
                    <li class="node1">
                        <NuxtLink to="/faq" class="menu_link">
                            <span>常見問題FAQ</span>
                        </NuxtLink>
                    </li>
                </ul>
            </nav>

            <div class="util_wrap">
                <a href="#" class="btn_cart" @click.prevent="openMiniCart">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                        <path
                            d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z" />
                    </svg>
                    <!-- 數量標籤 -->
                    <span v-if="cartTotalQty > 0" class="cart_badge">{{ cartTotalQty }}</span>
                </a>
                <NuxtLink v-if="!userCookie" to="/login" class="btn_login">
                    <span class="btn_text">登入</span>
                    <svg class="icon_user" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor"
                        stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </NuxtLink>
                <!-- 登入後顯示會員頭貼 -->
                <NuxtLink v-else to="/member" class="btn_login logged-in">
                    <img v-if="userCookie.avatar" :src="userCookie.avatar" alt="User Avatar" class="header-avatar">
                    <svg v-else class="icon_user" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor"
                        stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                    <span class="btn_text user-name">{{ userCookie.username || '會員中心' }}</span>
                </NuxtLink>
                <!-- 登出按鈕 (登入後才有) -->
                <button v-if="userCookie" @click="handleLogout" class="header-logout-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    登出
                </button>
            </div>

            <button type="button" class="btn_all_menu" :class="{ active: isMenuOpen }" @click.stop="toggleMenu">
                <i class="blind"></i>
                <div class="hamburger-lines">
                    <span class="line"></span>
                    <span class="line"></span>
                    <span class="line"></span>
                </div>
                <div class="icon_close">
                    <span class="line"></span>
                    <span class="line"></span>
                </div>
            </button>
        </div>
    </header>
    
    <!-- 全域小購物車側邊欄 -->
    <MiniCart />
</template>

<style scoped>
.btn_cart {
    position: relative;
}
.cart_badge {
    position: absolute;
    top: -2px;
    right: -2px;
    background-color: #e74c3c;
    color: #fff;
    font-size: 0.7rem;
    font-weight: bold;
    min-width: 18px;
    height: 18px;
    line-height: 18px;
    text-align: center;
    border-radius: 50%;
    border: 1px solid #fff;
    padding: 0 4px;
}

/* 登入後的按鈕樣式 */
.btn_login.logged-in {
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: none; /* 移除紫色內縮外框 */
    padding: 5px 10px;
}

/* 移除登入後按鈕 Hover 時原本的背景填補動畫 */
.btn_login.logged-in::before {
    display: none;
}

/* 改為單純的透明度 Hover 效果 */
.btn_login.logged-in:hover {
    box-shadow: none;
    background: transparent;
    opacity: 0.8;
    color: var(--grape-primary); /* 防止原本 hover 的文字變白設定生效 */
}

.header-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid rgba(0,0,0,0.1);
}
.user-name {
    max-width: 80px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: bold;
    font-size: 16px;
}

/* 頂端登出按鈕 */
.header-logout-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: 1px solid var(--grape-primary); /* 邊框與文字同色 */
    color: var(--grape-primary);
    padding: 6px 12px;
    border-radius: 6px; /* 這裡改為較方的圓角 6px */
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    /* 取消預設 button 樣式 */
    outline: none;
}
.header-logout-btn:hover {
    background: var(--grape-primary); /* Hover 填滿原本文字顏色的底色 */
    color: #fff; /* 文字變白色 */
    border-color: var(--grape-primary);
}

@media (max-width: 900px) {
    /* 在手機版隱藏文字只顯示圖示 */
    .header-logout-btn {
        width: 36px;
        height: 36px;
        padding: 5px;
        border: none;
        border-radius: 8px; /* 手機版也從圓圈改為微圓角的方型 */
        color: var(--grape-primary);
        justify-content: center;
        text-indent: 100%;
        white-space: nowrap;
        overflow: hidden;
    }
    .header-logout-btn svg {
        text-indent: 0;
        position: absolute;
    }
}
</style>
