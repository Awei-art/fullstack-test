<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '@/stores/cart' // 引入購物車 Store

const cartStore = useCartStore()

// 🔥 當網頁在瀏覽器掛載完成時，立刻去 LocalStorage 拿資料
onMounted(() => {
  console.log('App.vue: onMounted triggered, calling loadFromLocalStorage')
  cartStore.loadFromLocalStorage()
})
</script>

<template>

  <NuxtLayout>

    <NuxtPage />

  </NuxtLayout>
  
</template>