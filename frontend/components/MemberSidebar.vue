<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const menuItems = ref([
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
</script>


<template>
  <div class="sidebar-container">
    <ul class="menu-list">
      <li class="menu-item" v-for="item in menuItems" :key="item.name">
        <!-- Main menu link -->
        <NuxtLink :to="item.link" class="menu-link" :class="{ 'active': isParentActive(item) }">
          {{ item.name }}
        </NuxtLink>
        <!-- Sub menu list -->
        <ul v-if="item.subItems" class="sub-menu-list">
          <li v-for="sub in item.subItems" :key="sub.name">
            <NuxtLink :to="sub.link" class="sub-menu-link" exact-active-class="active">
              {{ sub.name }}
            </NuxtLink>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>



<style src="@/assets/css/MemberSidebar.css" scoped></style>
