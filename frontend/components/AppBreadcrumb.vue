<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    // Expected format: [{ name: '首頁', path: '/' }, { name: '葡萄商店', path: '/products' }, { name: '當前商品名稱' }]
  }
})
</script>

<template>
  <nav class="breadcrumb_container" aria-label="Breadcrumb">
    <ul class="breadcrumb_list">
      <li v-for="(item, index) in items" :key="index" class="breadcrumb_item">
        <!-- 若有 path 而且不是最後一項，就顯示連結 -->
        <NuxtLink v-if="item.path && index !== items.length - 1" :to="item.path" class="breadcrumb_link">
          {{ item.name }}
        </NuxtLink>
        <!-- 最後一項或是沒有 path，只顯示純文字 -->
        <span v-else class="breadcrumb_current" :aria-current="index === items.length - 1 ? 'page' : undefined">
          {{ item.name }}
        </span>
        
        <!-- 分隔符號 (除了最後一個 items 不用顯示) -->
        <span v-if="index !== items.length - 1" class="breadcrumb_separator">/</span>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.breadcrumb_container {
  padding: 10px 40px;
  max-width: 1200px;
  margin: 0 auto;
  margin-bottom: 20px; /* 給商品內容一點空間 */
}

.breadcrumb_list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.breadcrumb_item {
  display: flex;
  align-items: center;
}

.breadcrumb_link {
  color: #333;
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb_link:hover {
  text-decoration: underline;
  color: #c0392b; /* 品牌主色或紅色點綴 */
}

.breadcrumb_current {
  color: #999;
  cursor: default;
}

.breadcrumb_separator {
  margin: 0 10px;
  color: #ccc;
  font-size: 0.8rem;
}

@media (max-width: 768px) {
  .breadcrumb_container {
    padding: 10px 20px;
  }
  .breadcrumb_list {
    font-size: 0.85rem;
  }
}
</style>
