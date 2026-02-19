<script setup>
</script>

<template>
    <footer class="footer_section">
        <div class="footer_container">
            <div class="footer_content">
                <!-- SNS Column -->
                <div class="footer_col footer_sns">
                    <h3 class="footer_heading">社群媒體</h3>
                    <p class="footer_desc">最新消息請關注我們</p>
                    <div class="footer_social_icons">
                        <a href="https://www.instagram.com" target="_blank" class="social_link"><i
                                class="fab fa-instagram"></i></a>
                        <a href="https://www.facebook.com" target="_blank" class="social_link"><i
                                class="fab fa-facebook-f"></i></a>
                        <a href="https://line.me" target="_blank" class="social_link"><i class="fab fa-line"></i></a>
                    </div>
                </div>

                <!-- Links Column -->
                <div class="footer_col footer_links_col">
                    <ul class="footer_links">
                        <li><NuxtLink to="/">首頁</NuxtLink></li>
                        <li><NuxtLink to="#">關於我們</NuxtLink></li>
                        <li><NuxtLink to="#">商品販售</NuxtLink></li>
                        <li><NuxtLink to="#">農藥檢測</NuxtLink></li>
                        <li><NuxtLink to="#">線上商店</NuxtLink></li>
                        <li><NuxtLink to="#">人才招募</NuxtLink></li>
                    </ul>
                </div>

                <!-- Info Column -->
                <div class="footer_col footer_info">
                    <div class="footer_logo_wrap">
                        <img src="/images/田原葡萄-Logo.png" alt="Tianyuan Grape" class="footer_logo">
                        <span class="footer_brand_name">TIANYUAN GRAPE</span>
                    </div>
                    <div class="footer_contact">
                        <p>彰化縣大村鄉貢旗村大溪路13-51號</p>
                        <p>TEL：0975-404-672</p>
                    </div>
                </div>
            </div>
            <div class="footer_copyright">
                <p>Copyright © Tianyuan Grape</p>
            </div>
        </div>
    </footer>
</template>
