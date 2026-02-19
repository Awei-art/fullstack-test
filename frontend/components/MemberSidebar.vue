<script setup>
import { ref } from 'vue'

const menuItems = ref([
  { name: '帳號資訊', link: '/member' }, // Currently pointing to member home
  { name: '歷史訂單', link: '/member/orders' },
  { name: '我的優惠券', link: '/member/coupons' },
  { name: '收件地址管理', link: '/member/address' },
])
</script>


<template>
  <div class="sidebar-container">
    <div class="profile-section">
      <!-- Placeholder image if no user avatar provided -->
      <img src="https://ui-avatars.com/api/?name=Tian+Yuan&background=C1A96C&color=fff" alt="User Avatar" class="avatar" />
      <div class="user-name">王小明</div>
    </div>

    <ul class="menu-list">
      <li class="menu-item" v-for="item in menuItems" :key="item.name">
        <!-- Using a hash or placeholder link for now as sub-pages might not exist -->
        <NuxtLink :to="item.link" class="menu-link" exact-active-class="active">
          {{ item.name }}
        </NuxtLink>
      </li>
    </ul>

    <button class="logout-btn">
      登出
    </button>
  </div>
</template>



<style src="@/assets/css/MemberSidebar.css" scoped></style>
