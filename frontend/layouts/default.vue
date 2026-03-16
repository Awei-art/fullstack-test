<script setup>
const route = useRoute()
</script>

<template>
  <div>
    <SaleBanner v-if="route.path === '/'" />
    <AppHeader />

        <slot />
   
    <AppFooter />
  </div>
</template>