<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import MiniCart from '@/components/MiniCart.vue'

const route = useRoute()
const isMemberRoute = computed(() => route.path.startsWith('/member'))

// 會員中心選單清單
const memberMenuItems = ref([
  { 
    name: '帳號資訊', 
    link: '/member',
    subItems: [
      { name: '會員基本資料', link: '/member/profile' },
      { name: '修改登入密碼', link: '/member/password' }
    ]
  },
  { 
    name: '訂單狀態', 
    link: '/member/orders',
  },
  { name: '我的優惠券', link: '/member/coupons' },
  { name: '收件地址管理', link: '/member/address' },
])

const isParentActive = (item) => {
  if (route.path === item.link) return true;
  if (item.subItems) {
    return item.subItems.some(sub => route.path.startsWith(sub.link));
  }
  return false;
}

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

// 🔥 捲動偵測：控制手機版漢堡圖 & Logo 位置動畫
// 加入滯後 (hysteresis) 防止在臨界點反覆閃爍
const isScrolled = ref(false)
const handleScroll = () => {
    const y = window.scrollY
    if (!isScrolled.value && y > 80) {
        isScrolled.value = true
    } else if (isScrolled.value && y < 30) {
        isScrolled.value = false
    }
}

const isUserMenuOpen = ref(false)
const userMenuRef = ref(null)

const handleUserMenuClick = (e) => {
    // 手機版和桌機版都可以 toggle 選單
    isUserMenuOpen.value = !isUserMenuOpen.value
}

const closeUserMenu = () => {
    isUserMenuOpen.value = false
}

// 桌機版 Hover 顯示下拉選單（帶延遲避免閃爍）
let hoverTimer = null
const handleMouseEnter = () => {
    if (window.innerWidth > 900) {
        if (hoverTimer) clearTimeout(hoverTimer)
        isUserMenuOpen.value = true
    }
}
const handleMouseLeave = () => {
    if (window.innerWidth > 900) {
        hoverTimer = setTimeout(() => {
            isUserMenuOpen.value = false
        }, 300)
    }
}

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
    isMenuOpen.value = false
}

// 手機版子選單展開（如果是無法點擊的純展開選項）
const toggleSubmenu = (e) => {
    if (window.innerWidth <= 900) {
        e.preventDefault()
        const li = e.currentTarget.closest('.has_submenu')
        if (li) li.classList.toggle('open')
    }
}

// 支援「本身有連結、又帶有子選單」的手機版混合展開邏輯
const handleSubmenuLinkClick = (e) => {
    if (window.innerWidth <= 900) {
        const rect = e.currentTarget.getBoundingClientRect()
        const clickX = e.clientX
        
        // CSS 中箭頭寫在 ::after (right: 30px)
        // 若使用者點擊選單列最右側 80px 的區域，判定為「點下箭頭」，只展開不跳轉
        if (rect.right - clickX < 80) {
            e.preventDefault()
            const li = e.currentTarget.closest('.has_submenu')
            if (li) li.classList.toggle('open')
        } else {
            // 點擊左側文字區域，關閉選單並進行頁面跳轉
            closeMenu()
        }
    } else {
        // 電腦版直接關閉選單即可，Hover 本身就會觸發展開顯示
        closeMenu()
    }
}

const handleClickOutside = (event) => {
    // If menu is open and click is outside the header, close the menu
    if (isMenuOpen.value && headerRef.value && !headerRef.value.contains(event.target)) {
        closeMenu()
    }
    // Handle user menu click outside
    if (isUserMenuOpen.value && userMenuRef.value && !userMenuRef.value.contains(event.target)) {
        closeUserMenu()
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
    window.addEventListener('scroll', handleScroll, { passive: true })
    handleScroll()
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
    window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
    <header class="header_wrap grape-theme">
        <div class="header" :class="{ 'mobile-menu-open': isMenuOpen, 'scrolled': isScrolled, 'is-member-route': isMemberRoute }" ref="headerRef">
            <h1 class="logo">
                <NuxtLink to="/" class="logo_link">
                    <img src="/images/logo_icon.svg" alt="田原葡萄Icon" class="logo_icon">
                    <img src="/images/logo_text.svg" alt="田原溫室葡萄" class="logo_default">
                </NuxtLink>
            </h1>

            <nav>
                <ul class="header_menu_wrap" :style="{ display: isMenuOpen ? 'flex' : '' }">
                    <li class="mobile_menu_logo_item">
                        <NuxtLink to="/" @click="closeMenu">
                            <img src="/images/menu_header.png" alt="田原溫室">
                        </NuxtLink>
                    </li>
                    
                    <!-- 會員中心專屬導覽選單（僅在手機版 & 會員頁面顯示） -->
                    <li class="node1 member-nav-item" :class="{ 'has_submenu': item.subItems }" v-for="item in memberMenuItems" :key="item.name">
                        <!-- 如果有子選單 -->
                        <template v-if="item.subItems">
                            <NuxtLink :to="item.link" class="menu_link" :class="{ 'active': isParentActive(item) }" @click="handleSubmenuLinkClick">
                                <span>{{ item.name }}</span>
                            </NuxtLink>
                            <ul class="submenu">
                                <li v-for="sub in item.subItems" :key="sub.name">
                                    <NuxtLink :to="sub.link" class="menu_link" exact-active-class="active" @click="closeMenu">
                                        <span>{{ sub.name }}</span>
                                    </NuxtLink>
                                </li>
                            </ul>
                        </template>
                        <!-- 如果沒有子選單 -->
                        <template v-else>
                            <NuxtLink :to="item.link" class="menu_link" :class="{ 'active': isParentActive(item) }" @click="closeMenu">
                                <span>{{ item.name }}</span>
                            </NuxtLink>
                        </template>
                    </li>
                    
                    <!-- 普通導覽選單（在手機版會員頁面時會被隱藏） -->
                    <li class="node1 normal-nav-item">
                        <NuxtLink to="/news" class="menu_link" @click="closeMenu">
                            <span>最新消息</span>
                        </NuxtLink>
                    </li>
                    <li class="node1 normal-nav-item">
                        <NuxtLink to="/about" class="menu_link" @click="closeMenu">
                            <span>關於田原</span>
                        </NuxtLink>
                    </li>
                    <li class="node1 has_submenu normal-nav-item">
                        <a href="#" class="menu_link" @click.prevent="toggleSubmenu">
                            <span>線上商店</span>
                        </a>
                        <ul class="submenu">
                            <li>
                                <NuxtLink to="/products" class="menu_link" @click="closeMenu">
                                    <span>葡萄禮盒</span>
                                </NuxtLink>
                            </li>
                            <li>
                                <NuxtLink to="/desserts" class="menu_link" @click="closeMenu">
                                    <span>甜點專區</span>
                                </NuxtLink>
                            </li>
                        </ul>
                    </li>
                    <li class="node1 normal-nav-item">
                        <NuxtLink to="/varieties" class="menu_link" @click="closeMenu">
                            <span>品種介紹</span>
                        </NuxtLink>
                    </li>
                    <li class="node1 normal-nav-item">
                        <NuxtLink to="/faq" class="menu_link" @click="closeMenu">
                            <span>常見問題FAQ</span>
                        </NuxtLink>
                    </li>

                    <!-- 手機版漢堡選單內的會員區塊（滾動後頭貼消失時才顯示，但如果是會員中心專屬選單則不顯示） -->
                    <li v-if="isScrolled && !isMemberRoute" class="mobile_menu_user_area">
                        <template v-if="userCookie">
                            <NuxtLink to="/member" class="menu_user_info" @click="closeMenu">
                                <img v-if="userCookie.avatar" :src="userCookie.avatar" alt="User Avatar" class="menu_avatar">
                                <svg v-else class="menu_avatar_icon" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor"
                                    stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                    <circle cx="12" cy="7" r="4"></circle>
                                </svg>
                                <span class="menu_user_name">{{ userCookie.nickname || userCookie.username || '會員中心' }}</span>
                            </NuxtLink>
                            <button class="menu_logout_btn" @click="handleLogout">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                                    <polyline points="16 17 21 12 16 7"></polyline>
                                    <line x1="21" y1="12" x2="9" y2="12"></line>
                                </svg>
                                登出
                            </button>
                        </template>
                        <NuxtLink v-else to="/login" class="menu_login_btn" @click="closeMenu">
                            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor"
                                stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            登入
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
                <div v-else class="header-user-wrapper" ref="userMenuRef" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
                    <a href="#" class="btn_login logged-in" @click.prevent="handleUserMenuClick">
                        <img v-if="userCookie.avatar" :src="userCookie.avatar" alt="User Avatar" class="header-avatar">
                        <svg v-else class="icon_user" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor"
                            stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <span class="btn_text user-name desktop-only">{{ userCookie.username || '會員中心' }}</span>
                    </a>

                    <!-- 頭像下拉選單 (桌機 Hover / 手機 Click) -->
                    <transition name="fade">
                        <div v-show="isUserMenuOpen" class="user-dropdown">
                            <!-- 整合進來的購物車（僅手機版顯示） -->
                            <button @click="(e) => { closeUserMenu(); openMiniCart(e); }" class="dropdown-link mobile-only" style="width: 100%; border: none; background: transparent; cursor: pointer;">
                                <span style="position: relative; display: inline-block;">
                                    <span v-if="cartTotalQty > 0" class="cart_badge" style="position: absolute; top: -8px; left: auto; right: -18px; transform: none; margin: 0; display: flex; width: 20px; height: 20px; font-size: 11px; align-items: center; justify-content: center;">{{ cartTotalQty }}</span>
                                    購物車
                                </span>
                            </button>
                            <NuxtLink to="/member" class="dropdown-link" @click="closeUserMenu">會員中心</NuxtLink>
                            <button @click="handleLogout" class="dropdown-link text-danger">登出</button>
                        </div>
                    </transition>
                </div>
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

            <!-- 手機版遮罩：點擊黑色半透明背景可收起導覽列 -->
            <div v-if="isMenuOpen" class="mobile-overlay" @click="closeMenu"></div>
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

.header-user-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.user-dropdown {
    display: flex; /* V-show 會直接控制這個元件 */
    position: absolute;
    top: 50px;
    right: 0;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    width: 120px;
    flex-direction: column;
    overflow: hidden;
    z-index: 1000;
}

/* Add an active state for the user head */
.btn_login.logged-in:active {
    opacity: 0.6;
}

.dropdown-link {
    display: block;
    padding: 12px 16px;
    text-align: center;
    color: #333;
    font-size: 14px;
    border-bottom: 1px solid #eee;
    background: none;
    border: none;
    width: 100%;
    cursor: pointer;
    text-decoration: none;
}

.dropdown-link:last-child {
    border-bottom: none;
}

.dropdown-link.text-danger {
    color: #e74c3c;
    font-weight: bold;
}

/* 僅手機版顯示的元素 */
.mobile-only {
    display: none !important;
}

@media (max-width: 900px) {
    /* 隱藏桌機版專屬按鈕與文字 */
    .desktop-only {
        display: none !important;
    }

    /* 顯示手機版專屬元素 */
    .mobile-only {
        display: block !important;
    }

    /* 放大手機版的購物車與頭像圖示 */
    .btn_cart {
        margin-right: 15px; /* 控制購物車向左退 (數字越大退越多) */
    }

    .btn_cart svg {
        width: 28px;
        height: 28px;
    }

    .header-avatar {
        width: 38px;
        height: 38px;
    }

    .icon_user {
        width: 28px;
        height: 28px;
    }
}
</style>
