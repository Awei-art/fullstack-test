<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

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
                <NuxtLink to="/cart" class="btn_cart">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                        <path
                            d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z" />
                    </svg>
                </NuxtLink>
                <NuxtLink to="/login" class="btn_login">
                    <span class="btn_text">登入</span>
                    <svg class="icon_user" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor"
                        stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </NuxtLink>
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
</template>
