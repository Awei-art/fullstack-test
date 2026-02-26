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
    <ul class="menu-list">
      <li class="menu-item" v-for="item in menuItems" :key="item.name">
        <!-- Using a hash or placeholder link for now as sub-pages might not exist -->
        <NuxtLink :to="item.link" class="menu-link" exact-active-class="active">
          {{ item.name }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>



<style src="@/assets/css/MemberSidebar.css" scoped></style>
