<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  totalBoxes: { type: Number, required: true },
  totalPrice: { type: Number, required: true }
})

const emit = defineEmits(['update:shippingFee'])

// 使用者輸入地址數量，預設為 1
const addressCount = ref(1)

// 計算運費的函數
const calculatedShipping = computed(() => {
  if (props.totalBoxes === 0) return 0
  
  // 1. 將盒子盡量平均分配給輸入的地址數量
  const baseBoxes = Math.floor(props.totalBoxes / addressCount.value)
  const remainderAddresses = props.totalBoxes % addressCount.value

  // 取得單個盒子的平均金額，以便判斷是否滿足金額門檻 (滿 1250 / 2500)
  const avgPrice = props.totalPrice / props.totalBoxes

  let packages = []

  for (let i = 0; i < addressCount.value; i++) {
    // 每個地址分到的總盒數
    let addressBoxes = baseBoxes + (i < remainderAddresses ? 1 : 0)
    
    // 一件包裹最多只能裝 4 盒，因此將該地址的盒子分拆成多個包裹
    while (addressBoxes > 0) {
      const pkgBoxes = Math.min(4, addressBoxes)
      packages.push(pkgBoxes)
      addressBoxes -= pkgBoxes
    }
  }

  // 2. 對每個包裹個別計算應收運費
  let fees = packages.map(pkgBoxes => {
    const pkgPrice = pkgBoxes * avgPrice
    // 滿2500 或 滿4盒 -> 一個地址免運費
    if (pkgBoxes >= 4 || pkgPrice >= 2500) return 0
    // 滿1250 或 滿2盒 -> 運費 150
    if (pkgBoxes >= 2 || pkgPrice >= 1250) return 150
    // 其他 -> 運費 230
    return 230
  })

  // 3. 特殊滿額條件：總盒數 >= 10 盒，本來剩下那件需150(或230)直接變成免運
  if (props.totalBoxes >= 10) {
    // 找出所有非零的運費包裹
    let nonZeroFees = fees.filter(fee => fee > 0)
    if (nonZeroFees.length > 0) {
      // 找到其中最貴的（通常是 230 或 150）將其折抵掉
      let maxFee = Math.max(...nonZeroFees)
      let targetIndex = fees.indexOf(maxFee)
      if (targetIndex !== -1) {
        fees[targetIndex] = 0
      }
    }
  }

  // 4. 加總所有包裹費用
  return fees.reduce((sum, fee) => sum + fee, 0)
})

// 當有變化時，將最新運費傳遞回大購物車的總結帳台
watch(calculatedShipping, (newFee) => {
  emit('update:shippingFee', newFee)
}, { immediate: true })

// 增加/減少地址數量
const addAddress = () => { addressCount.value++ }
const minusAddress = () => { 
  if (addressCount.value > 1) addressCount.value-- 
}

// 產生動態促銷提示訊息
const promoMessage = computed(() => {
  if (props.totalBoxes === 0) return '消費滿額或滿 4 盒，即可享一個地址免運優惠！'
  
  if (calculatedShipping.value === 0) {
    if (addressCount.value > 1) {
      return '太棒了！您目前的購買組合已讓所有地址完全免運！'
    } else {
      return '已達免運門檻！省下了一筆運費 🎉'
    }
  } else {
    // 若還有未免運的包裹，提醒差幾盒或差多少錢
    let remainderBoxes = props.totalBoxes % 4
    if (remainderBoxes === 0) {
      return '若要加開更多免運件，請繼續累積盒數或金額！'
    } else {
      let diffBoxes = 4 - remainderBoxes
      // 每盒平均單價若較低，顯示差額會激勵消費
      let diffPrice = 2500 - ((props.totalPrice / props.totalBoxes) * remainderBoxes)
      if (diffPrice < 0) diffPrice = 2500 // 防呆
      
      let priceStr = Math.round(diffPrice).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
      return `【促銷】再買 ${diffBoxes} 盒，或該包裹消費再加 NT$ ${priceStr}，即可再享一包裹免運！`
    }
  }
})
</script>

<template>
  <div class="shipping_calculator">
    <div class="calc_header">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="1" y="3" width="15" height="13"></rect>
        <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
        <circle cx="5.5" cy="18.5" r="2.5"></circle>
        <circle cx="18.5" cy="18.5" r="2.5"></circle>
      </svg>
      <h3>多地址運費計算試算</h3>
    </div>
    
    <div class="calc_body">
      <div class="calc_row input_group">
        <span>欲寄送的地址數量：</span>
        <div class="qty_control">
          <button @click="minusAddress" :disabled="addressCount <= 1">-</button>
          <span>{{ addressCount }}</span>
          <button @click="addAddress" :disabled="addressCount >= totalBoxes && totalBoxes > 0">+</button>
        </div>
      </div>
      <p class="address_hint">※ 一件包裹最多 4 盒，滿額退減將自動由系統選取最佳方案為您折抵。</p>
      
      <div class="calc_row result_row">
        <span>試算運費：</span>
        <strong class="shipping_price" v-if="calculatedShipping > 0">
          NT$ {{ calculatedShipping.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}
        </strong>
        <strong class="shipping_price free_tag" v-else>
          免運費
        </strong>
      </div>
    </div>
    
    <div class="promo_notice" :class="{ 'promo_active': calculatedShipping === 0 && totalBoxes > 0 }">
      {{ promoMessage }}
    </div>
  </div>
</template>

<style scoped>
.shipping_calculator {
  background-color: #fdfbf7;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 20px;
  margin: 15px 0 25px 0;
  font-family: 'Times New Roman', 'Noto Sans TC', sans-serif;
}

.calc_header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid #333;
  padding-bottom: 10px;
}

.calc_header svg {
  color: #C5374E;
}

.calc_header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #111;
  font-weight: 500;
  letter-spacing: 1px;
}

.calc_body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.calc_row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
  color: #555;
}

.input_group {
  margin-top: 5px;
}

.qty_control {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  overflow: hidden;
  background: #fff;
  height: 36px;
}

.qty_control button {
  background: #fff;
  border: none;
  width: 36px;
  height: 100%;
  cursor: pointer;
  color: #333;
  font-size: 1.2rem;
  transition: background 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.qty_control button:hover:not(:disabled) {
  background: #f0f0f0;
}

.qty_control button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.qty_control span {
  width: 45px;
  text-align: center;
  font-size: 1rem;
  color: #111;
  font-weight: bold;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.address_hint {
  font-size: 0.8rem;
  color: #888;
  margin: 0;
  line-height: 1.5;
}

.result_row {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px dashed #ccc;
}

.shipping_price {
  font-size: 1.25rem;
  color: #000;
  font-weight: bold;
}

.free_tag {
  color: #C5374E; /* 酒紅色 highlight 免運 */
}

.promo_notice {
  margin-top: 20px;
  padding: 12px;
  background-color: #fdf5f5;
  color: #C5374E;
  font-size: 0.9rem;
  text-align: center;
  border: 1px dotted #eba0a0;
  line-height: 1.5;
}

.promo_active {
  background-color: #f4fdf8;
  color: #27ae60;
  border-color: #a3e4d7;
}

</style>
