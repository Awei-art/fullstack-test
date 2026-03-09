<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useCartStore } from '@/stores/cart'

definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const config = useRuntimeConfig()
const router = useRouter()
const userCookie = useCookie('user_info')
const cartStore = useCartStore()

// === 狀態 ===
const isSubmitting = ref(false)
const errorMessage = ref('')
const savedAddresses = ref([])

// 付款方式 & 備註
const paymentMethod = ref('cod')
const orderNote = ref('')

// === 優惠券 ===
const couponCodeInput = ref('')
const couponMessage = ref({ text: '', type: '' })
const isApplyingCoupon = ref(false)

// 台灣縣市鄉鎮資料
const taiwanCities = {
  '基隆市': ['仁愛區', '信義區', '中正區', '中山區', '安樂區', '暖暖區', '七堵區'],
  '台北市': ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'],
  '新北市': ['萬里區', '金山區', '板橋區', '汐止區', '深坑區', '石碇區', '瑞芳區', '平溪區', '雙溪區', '貢寮區', '新店區', '坪林區', '烏來區', '永和區', '中和區', '土城區', '三峽區', '樹林區', '鶯歌區', '三重區', '新莊區', '泰山區', '林口區', '蘆洲區', '五股區', '八里區', '淡水區', '三芝區', '石門區'],
  '桃園市': ['中壢區', '平鎮區', '龍潭區', '楊梅區', '新屋區', '觀音區', '桃園區', '龜山區', '八德區', '大溪區', '復興區', '大園區', '蘆竹區'],
  '新竹市': ['東區', '北區', '香山區'],
  '新竹縣': ['竹北市', '湖口鄉', '新豐鄉', '新埔鎮', '關西鎮', '芎林鄉', '寶山鄉', '竹東鎮', '五峰鄉', '橫山鄉', '尖石鄉', '北埔鄉', '峨眉鄉'],
  '苗栗縣': ['竹南鎮', '頭份市', '三灣鄉', '南庄鄉', '獅潭鄉', '後龍鎮', '通霄鎮', '苑裡鎮', '苗栗市', '造橋鄉', '頭屋鄉', '公館鄉', '大湖鄉', '泰安鄉', '銅鑼鄉', '三義鄉', '西湖鄉', '卓蘭鎮'],
  '台中市': ['中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區', '霧峰區', '烏日區', '豐原區', '后里區', '石岡區', '東勢區', '和平區', '新社區', '潭子區', '大雅區', '神岡區', '大肚區', '沙鹿區', '龍井區', '梧棲區', '清水區', '大甲區', '外埔區', '大安區'],
  '彰化縣': ['彰化市', '芬園鄉', '花壇鄉', '秀水鄉', '鹿港鎮', '福興鄉', '線西鄉', '和美鎮', '伸港鄉', '員林市', '社頭鄉', '永靖鄉', '埔心鄉', '溪湖鎮', '大村鄉', '埔鹽鄉', '田中鎮', '北斗鎮', '田尾鄉', '埤頭鄉', '溪州鄉', '竹塘鄉', '二林鎮', '大城鄉', '芳苑鄉', '二水鄉'],
  '南投縣': ['南投市', '中寮鄉', '草屯鎮', '國姓鄉', '埔里鎮', '仁愛鄉', '名間鄉', '集集鎮', '水里鄉', '魚池鄉', '信義鄉', '竹山鎮', '鹿谷鄉'],
  '雲林縣': ['斗南鎮', '大埤鄉', '虎尾鎮', '土庫鎮', '褒忠鄉', '東勢鄉', '臺西鄉', '崙背鄉', '麥寮鄉', '斗六市', '林內鄉', '古坑鄉', '莿桐鄉', '西螺鎮', '二崙鄉', '北港鎮', '水林鄉', '口湖鄉', '四湖鄉', '元長鄉'],
  '嘉義市': ['東區', '西區'],
  '嘉義縣': ['番路鄉', '梅山鄉', '竹崎鄉', '阿里山鄉', '中埔鄉', '大埔鄉', '水上鄉', '鹿草鄉', '太保市', '朴子市', '東石鄉', '六腳鄉', '新港鄉', '民雄鄉', '大林鎮', '溪口鄉', '義竹鄉', '布袋鎮'],
  '台南市': ['中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區', '安定區'],
  '高雄市': ['新興區', '前金區', '苓雅區', '鹽埕區', '鼓山區', '旗津區', '前鎮區', '三民區', '楠梓區', '小港區', '左營區', '仁武區', '大社區', '岡山區', '路竹區', '阿蓮區', '田寮區', '燕巢區', '橋頭區', '梓官區', '彌陀區', '永安區', '湖內區', '鳳山區', '大寮區', '林園區', '鳥松區', '大樹區', '旗山區', '美濃區', '六龜區', '內門區', '杉林區', '甲仙區', '桃源區', '那瑪夏區', '茂林區'],
  '屏東縣': ['屏東市', '三地門鄉', '霧臺鄉', '瑪家鄉', '九如鄉', '里港鄉', '高樹鄉', '鹽埔鄉', '長治鄉', '麟洛鄉', '竹田鄉', '內埔鄉', '萬丹鄉', '潮州鎮', '泰武鄉', '來義鄉', '萬巒鄉', '崁頂鄉', '新埤鄉', '南州鄉', '林邊鄉', '東港鎮', '琉球鄉', '佳冬鄉', '新園鄉', '枋寮鄉', '枋山鄉', '春日鄉', '獅子鄉', '車城鄉', '牡丹鄉', '恆春鎮', '滿州鄉'],
  '宜蘭縣': ['宜蘭市', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '羅東鎮', '三星鄉', '大同鄉', '五結鄉', '冬山鄉', '蘇澳鎮', '南澳鄉'],
  '花蓮縣': ['花蓮市', '新城鄉', '秀林鄉', '吉安鄉', '壽豐鄉', '鳳林鎮', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉', '玉里鎮', '卓溪鄉', '富里鄉'],
  '台東縣': ['臺東市', '綠島鄉', '蘭嶼鄉', '延平鄉', '卑南鄉', '鹿野鄉', '關山鎮', '海端鄉', '池上鄉', '東河鄉', '成功鎮', '長濱鄉', '太麻里鄉', '金峰鄉', '大武鄉', '達仁鄉'],
  '澎湖縣': ['馬公市', '西嶼鄉', '望安鄉', '七美鄉', '白沙鄉', '湖西鄉'],
  '金門縣': ['金沙鎮', '金湖鎮', '金寧鄉', '金城鎮', '烈嶼鄉', '烏坵鄉'],
  '連江縣': ['南竿鄉', '北竿鄉', '莒光鄉', '東引鄉']
}

// ============================================
// 多地址寄送系統
// ============================================
const shippingGroups = ref([])

// 建立一筆新的寄送群組
function createShippingGroup(addressData = null) {
  return {
    id: Date.now() + Math.random(), // 唯一 key
    mode: 'book', // 'book' | 'manual'
    selectedAddressId: null,
    form: {
      receiver_name: '',
      receiver_phone: '',
      city: '',
      district: '',
      address: '',
    },
    boxCount: 0,
  }
}

// 新增寄送地址（自動從盒數最多的群組借 1 盒）
function addShippingGroup() {
  // 找出盒數最多的群組，借 1 盒給新地址
  const maxGroup = shippingGroups.value.reduce((max, g) => g.boxCount > max.boxCount ? g : max, shippingGroups.value[0])
  if (maxGroup.boxCount <= 1) {
    // 如果沒有任何群組有多餘的盒可以借，就不能新增
    return
  }
  maxGroup.boxCount -= 1
  const newGroup = createShippingGroup()
  newGroup.boxCount = 1
  shippingGroups.value.push(newGroup)
}

// 刪除寄送地址（至少保留 1 筆）
function removeShippingGroup(index) {
  if (shippingGroups.value.length <= 1) return
  const removedBoxes = shippingGroups.value[index].boxCount
  shippingGroups.value.splice(index, 1)
  // 把被移除的盒數加回第一筆
  if (removedBoxes > 0) {
    shippingGroups.value[0].boxCount += removedBoxes
  }
}

// 從地址簿套用到群組
function applyAddressToGroup(group, addr) {
  group.form.receiver_name = addr.receiver_name
  group.form.receiver_phone = addr.receiver_phone
  group.form.city = addr.city
  nextTick(() => {
    group.form.district = addr.district
  })
  group.form.address = addr.detail_address
}

// 監聽地址簿選擇
function onGroupAddressChange(group) {
  if (group.mode === 'book' && group.selectedAddressId) {
    const addr = savedAddresses.value.find(a => a.id === group.selectedAddressId)
    if (addr) applyAddressToGroup(group, addr)
  }
}

// 切換模式時
function onGroupModeChange(group, mode) {
  group.mode = mode
  if (mode === 'manual') {
    group.selectedAddressId = null
    group.form = { receiver_name: '', receiver_phone: '', city: '', district: '', address: '' }
  }
}

// 取得群組的可選鄉鎮
function getGroupDistricts(group) {
  return group.form.city ? (taiwanCities[group.form.city] || []) : []
}

// 城市變更時清空鄉鎮
function onGroupCityChange(group) {
  group.form.district = ''
}

// 檢查群組是否填寫完整
function isGroupComplete(group) {
  return (
    group.form.receiver_name.trim() &&
    group.form.receiver_phone.trim() &&
    group.form.city &&
    group.form.district &&
    group.form.address.trim()
  )
}

// 取得地址簿預覽
function getGroupAddressPreview(group) {
  if (group.mode !== 'book' || !group.selectedAddressId) return null
  return savedAddresses.value.find(a => a.id === group.selectedAddressId)
}

// === 盒數分配 ===
const totalAllocated = computed(() => {
  return shippingGroups.value.reduce((sum, g) => sum + g.boxCount, 0)
})

const remainingBoxes = computed(() => {
  return totalQuantity.value - totalAllocated.value
})

const isFullyAllocated = computed(() => {
  return totalQuantity.value > 0 && remainingBoxes.value === 0
})

// 每個群組的最大可分配盒數
function getMaxBoxCount(index) {
  const current = shippingGroups.value[index].boxCount
  return current + remainingBoxes.value
}

// 是否可以新增地址（至少要有一個群組 > 1 盒 才能分出 1 盒給新地址）
const canAddGroup = computed(() => {
  return shippingGroups.value.some(g => g.boxCount > 1)
})

// === 購物車資料 ===
const userCoupons = ref([])

onMounted(async () => {
  cartStore.loadFromLocalStorage()
  fetchAddresses()
  await fetchMyCoupons()
  
  // 載入時若有保留的優惠代碼，設定好 input value，這裡稍後會自動觸發 watch
  if (cartStore.couponCode) {
    couponCodeInput.value = cartStore.couponCode
  }
})

// 取得會員錢包的優惠券
async function fetchMyCoupons() {
  try {
    const user = userCookie.value
    if (!user?.token) return
    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/coupons/my/`, {
      headers: { Authorization: `Bearer ${user.token}` }
    })
    // 只保留「可使用」的優惠券
    userCoupons.value = res.filter(c => c.status_msg === '可使用')
  } catch (e) {
    console.error('取得錢包優惠券失敗:', e)
  }
}

const cartItems = computed(() => cartStore.items)
const totalQuantity = computed(() => cartStore.totalQty)
const subtotal = computed(() => cartStore.totalPrice)

// 有效的寄送群組（盒數 > 0 的才算）
const activeGroups = computed(() => {
  return shippingGroups.value.filter(g => g.boxCount > 0)
})

// 運費計算（多地址版本，只計算有效群組）
const shippingFee = computed(() => {
  const totalBoxes = totalQuantity.value
  const tPrice = subtotal.value
  if (totalBoxes === 0) return 0

  const avgPrice = tPrice / totalBoxes
  
  // 根據有效的多地址分配產生包裹（忽略盒數 0 的地址）
  let packages = []
  for (const group of activeGroups.value) {
    let boxes = group.boxCount
    while (boxes > 0) {
      const pkgBoxes = Math.min(4, boxes)
      packages.push(pkgBoxes)
      boxes -= pkgBoxes
    }
  }

  // 如果還沒分配完，用預設邏輯
  if (packages.length === 0) {
    let remainBoxes = totalBoxes
    while (remainBoxes > 0) {
      const pkgBoxes = Math.min(4, remainBoxes)
      packages.push(pkgBoxes)
      remainBoxes -= pkgBoxes
    }
  }

  let fees = packages.map(pkgBoxes => {
    const pkgPrice = pkgBoxes * avgPrice
    if (pkgBoxes >= 4 || pkgPrice >= 2500) return 0
    if (pkgBoxes >= 2 || pkgPrice >= 1250) return 150
    return 230
  })

  const boxFreeCount = totalBoxes >= 10 ? Math.ceil(totalBoxes / 4) : 0
  const priceFreeCount = Math.floor(tPrice / 2500)
  const freeCount = Math.max(boxFreeCount, priceFreeCount)

  if (freeCount > 0) {
    for (let i = 0; i < Math.min(freeCount, fees.length); i++) {
      fees[i] = 0
    }
  }

  return fees.reduce((sum, fee) => sum + fee, 0)
})

// 包裹資訊
const packageInfo = computed(() => {
  const totalBoxes = totalQuantity.value
  if (totalBoxes === 0) return { total: 0, free: 0 }

  const avgPrice = subtotal.value / totalBoxes
  let packages = []
  
  for (const group of activeGroups.value) {
    let boxes = group.boxCount
    while (boxes > 0) {
      const pkgBoxes = Math.min(4, boxes)
      packages.push(pkgBoxes)
      boxes -= pkgBoxes
    }
  }

  if (packages.length === 0) {
    let remainBoxes = totalBoxes
    while (remainBoxes > 0) {
      const pkgBoxes = Math.min(4, remainBoxes)
      packages.push(pkgBoxes)
      remainBoxes -= pkgBoxes
    }
  }

  let fees = packages.map(pkgBoxes => {
    const pkgPrice = pkgBoxes * avgPrice
    if (pkgBoxes >= 4 || pkgPrice >= 2500) return 0
    if (pkgBoxes >= 2 || pkgPrice >= 1250) return 150
    return 230
  })

  const boxFree = totalBoxes >= 10 ? Math.ceil(totalBoxes / 4) : 0
  const priceFree = Math.floor(subtotal.value / 2500)
  const freeCount = Math.max(boxFree, priceFree)

  if (freeCount > 0) {
    for (let i = 0; i < Math.min(freeCount, fees.length); i++) {
      fees[i] = 0
    }
  }

  const freePackages = fees.filter(f => f === 0).length
  return { total: packages.length, free: freePackages }
})

const totalAmount = computed(() => {
  const calc = subtotal.value + shippingFee.value - cartStore.discountAmount
  return calc < 0 ? 0 : calc
})

// === 優惠券處理 ===
// 單獨拉出驗證邏輯，方便手動與自動呼叫
async function validateAndApplyCoupon(code) {
  if (!code) return false
  
  isApplyingCoupon.value = true
  
  try {
    const user = userCookie.value
    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    
    const res = await $fetch(`${apiBase}/coupons/validate/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${user?.token || ''}`,
        'Content-Type': 'application/json'
      },
      body: {
        coupon_code: code,
        subtotal: subtotal.value,
        shipping_fee: shippingFee.value
      }
    })
    
    if (res.valid) {
      cartStore.setCoupon(code, res.title, res.discount_amount)
      return { success: true, message: res.message || '套用成功！' }
    }
  } catch (e) {
    cartStore.removeCoupon()
    const errorMsg = e.data?.error || '優惠碼無效或已過期'
    return { success: false, message: errorMsg }
  } finally {
    isApplyingCoupon.value = false
  }
}

// 監聽金額變化，如果購物車增減導致小計改變，自動重新計算優惠券折扣
watch([subtotal, shippingFee], async (newValues, oldValues) => {
  // 如果載入中，不重複觸發
  if (isApplyingCoupon.value) return

  if (cartStore.couponCode) {
    const res = await validateAndApplyCoupon(cartStore.couponCode)
    if (!res?.success) {
      // 條件不符(例如低消沒過)，自動移除並提示
      couponCodeInput.value = ''
      couponMessage.value = { text: res ? res.message : '購物車變更，優惠碼已失效', type: 'error' }
    }
  }
}, { immediate: true })

// === 優惠券處理 ===
async function applyCoupon() {
  // 如果下拉選單選擇了空值（不使用優惠券），則移除
  if (!couponCodeInput.value || !couponCodeInput.value.trim()) {
      removeCoupon()
      return
  }
  
  couponMessage.value = { text: '', type: '' }
  const res = await validateAndApplyCoupon(couponCodeInput.value.trim())
  
  if (res?.success) {
    couponMessage.value = { text: res.message, type: 'success' }
  } else {
    couponMessage.value = { text: res?.message || '驗證失敗', type: 'error' }
    // 驗證失敗的話，拔除異常代碼，恢復下拉選單的預設值
    couponCodeInput.value = ''
  }
}

function removeCoupon() {
  cartStore.removeCoupon()
  couponCodeInput.value = ''
  couponMessage.value = { text: '', type: '' } // 移除就不顯示提示
}

const formatPrice = (price) => {
  return 'NT$ ' + price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// === 載入地址簿 ===
async function fetchAddresses() {
  try {
    const user = userCookie.value
    if (!user?.token) return

    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase
    const res = await $fetch(`${apiBase}/address/`, {
      headers: { Authorization: `Bearer ${user.token}` }
    })

    savedAddresses.value = res

    // 初始化第一筆寄送群組，預設帶入預設地址 & 全部盒數
    const firstGroup = createShippingGroup()
    const defaultAddr = res.find(a => a.is_default)
    if (defaultAddr) {
      firstGroup.selectedAddressId = defaultAddr.id
      firstGroup.form.receiver_name = defaultAddr.receiver_name
      firstGroup.form.receiver_phone = defaultAddr.receiver_phone
      firstGroup.form.city = defaultAddr.city
      firstGroup.form.district = defaultAddr.district
      firstGroup.form.address = defaultAddr.detail_address
    }
    firstGroup.boxCount = totalQuantity.value
    shippingGroups.value = [firstGroup]
  } catch (e) {
    console.error('載入地址簿失敗:', e)
    // 即使載入失敗也要建立第一筆
    const firstGroup = createShippingGroup()
    firstGroup.mode = 'manual'
    firstGroup.boxCount = totalQuantity.value
    shippingGroups.value = [firstGroup]
  }
}

// 監聽購物車數量變化，自動調整第一筆
watch(totalQuantity, (newQty) => {
  if (shippingGroups.value.length > 0) {
    const allocated = shippingGroups.value.reduce((sum, g) => sum + g.boxCount, 0)
    const diff = newQty - allocated
    if (diff !== 0) {
      shippingGroups.value[0].boxCount = Math.max(0, shippingGroups.value[0].boxCount + diff)
    }
  }
})

// === 驗證 ===
// 只驗證盒數 > 0 的群組，盒數 0 的視為不存在
const isAllGroupsValid = computed(() => {
  return activeGroups.value.length > 0 && activeGroups.value.every(g => {
    return (
      g.form.receiver_name.trim() &&
      g.form.receiver_phone.trim() &&
      g.form.city &&
      g.form.district &&
      g.form.address.trim()
    )
  })
})

const isFormValid = computed(() => {
  return (
    cartItems.value.length > 0 &&
    isFullyAllocated.value &&
    isAllGroupsValid.value
  )
})

// === 提交訂單 ===
async function submitOrder() {
  if (!isFormValid.value || isSubmitting.value) return

  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const user = userCookie.value
    if (!user?.token) {
      errorMessage.value = '請先登入後再結帳'
      return
    }

    const apiBase = process.client ? config.public.apiBaseClient : config.public.apiBase

    // 組裝訂單品項
    const items = cartItems.value.map(item => ({
      item_type: item.itemType || 'product', // 傳送商品類型，讓後端區分葡萄或大福
      product_id: typeof item.id === 'string' ? parseInt(item.id.replace(/^(dessert-|product-)/, '')) : item.id,
      grade_id: item.gradeId || null,
      quantity: item.quantity,
      variety_names: item.varieties
        ? item.varieties.map(v => v.name).join('、')
        : '',
      product_image: item.image || '',
    }))

    // 只保留盒數 > 0 的地址（盒數 0 的視為不存在）
    const validGroups = activeGroups.value
    const primaryGroup = validGroups[0]

    // 組裝多寄送地址資訊（附在備註或延伸欄位）
    let shippingNote = orderNote.value
    if (validGroups.length > 1) {
      const groupDetails = validGroups.map((g, i) => {
        return `寄送${i + 1}: ${g.form.receiver_name} / ${g.form.receiver_phone} / ${g.form.city}${g.form.district}${g.form.address} (${g.boxCount}盒)`
      }).join('\n')
      shippingNote = shippingNote
        ? `${shippingNote}\n\n【多地址寄送明細】\n${groupDetails}`
        : `【多地址寄送明細】\n${groupDetails}`
    }

    const orderData = {
      receiver_name: primaryGroup.form.receiver_name,
      receiver_phone: primaryGroup.form.receiver_phone,
      shipping_city: primaryGroup.form.city,
      shipping_district: primaryGroup.form.district,
      shipping_address: primaryGroup.form.address,
      payment_method: paymentMethod.value,
      coupon_code: cartStore.couponCode,
      note: shippingNote,
      shipping_fee: shippingFee.value,
      items
    }

    const res = await $fetch(`${apiBase}/orders/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${user.token}`,
        'Content-Type': 'application/json'
      },
      body: orderData
    })

    // 成功！清空購物車
    cartStore.clearCart()

    // 信用卡付款 → 跳轉 ECPay
    if (res.payment) {
      // 建立隱藏表單，自動提交到 ECPay
      const form = document.createElement('form')
      form.method = 'POST'
      form.action = res.payment.payment_url
      form.style.display = 'none'

      for (const [key, value] of Object.entries(res.payment.params)) {
        const input = document.createElement('input')
        input.type = 'hidden'
        input.name = key
        input.value = value
        form.appendChild(input)
      }

      document.body.appendChild(form)
      form.submit()
      return
    }

    // 非信用卡 → 跳轉成功頁
    router.push({
      path: '/checkout/success',
      query: { order: res.order.order_number }
    })

  } catch (e) {
    console.error('下單失敗:', e)
    if (e.data) {
      const errData = e.data
      if (typeof errData === 'string') {
        errorMessage.value = errData
      } else if (errData.error) {
        errorMessage.value = errData.error
      } else if (errData.items) {
        errorMessage.value = Array.isArray(errData.items) ? errData.items[0] : errData.items
      } else {
        errorMessage.value = '下單失敗，請稍後再試'
      }
    } else {
      errorMessage.value = '網路連線異常，請稍後再試'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="checkout_page">
    <h1 class="checkout_title">結帳</h1>

    <ClientOnly>
      <div v-if="cartItems.length === 0" class="checkout_empty">
        <i class="fas fa-shopping-cart"></i>
        <p>您的購物車是空的，無法結帳</p>
        <NuxtLink to="/cart" class="back_to_cart_btn">前往購物車</NuxtLink>
      </div>

      <div v-else class="checkout_container">
        <!-- ====== 左欄 ====== -->
        <div class="checkout_left">

          <div v-if="errorMessage" class="error_msg">
            <i class="fas fa-exclamation-circle"></i> {{ errorMessage }}
          </div>

          <!-- 1. 多地址寄送 -->
          <div class="checkout_section">
            <div class="section_header">
              <i class="fas fa-map-marker-alt"></i>
              <h2>收件資訊</h2>
              <span class="address_count_badge" v-if="shippingGroups.length > 1">
                {{ shippingGroups.length }} 個地址
              </span>
            </div>

            <!-- 每一筆寄送群組 -->
            <div
              v-for="(group, index) in shippingGroups"
              :key="group.id"
              class="shipping_group"
              :class="{ 'has_border': shippingGroups.length > 1, 'incomplete': shippingGroups.length > 1 && !isGroupComplete(group) }"
            >
              <!-- 群組標頭 -->
              <div class="group_header" v-if="shippingGroups.length > 1">
                <span class="group_label">
                  📦 寄送地址 {{ index + 1 }}
                  <span v-if="!isGroupComplete(group)" class="group_incomplete_hint">← 請填寫收件資訊</span>
                </span>
                <button
                  v-if="index > 0"
                  class="group_remove_btn"
                  @click="removeShippingGroup(index)"
                  title="移除此寄送地址"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>

              <!-- 地址來源切換 -->
              <div class="address_tabs">
                <button
                  class="address_tab"
                  :class="{ active: group.mode === 'book' }"
                  @click="onGroupModeChange(group, 'book')"
                >
                  從地址簿選取
                </button>
                <button
                  class="address_tab"
                  :class="{ active: group.mode === 'manual' }"
                  @click="onGroupModeChange(group, 'manual')"
                >
                  手動填寫
                </button>
              </div>

              <!-- 地址簿 -->
              <div v-if="group.mode === 'book'">
                <select
                  v-model="group.selectedAddressId"
                  class="address_book_select"
                  @change="onGroupAddressChange(group)"
                >
                  <option :value="null" disabled>請選擇收件地址</option>
                  <option v-for="addr in savedAddresses" :key="addr.id" :value="addr.id">
                    {{ addr.title ? `[${addr.title}] ` : '' }}{{ addr.receiver_name }} - {{ addr.city }}{{ addr.district }}{{ addr.detail_address }}
                    {{ addr.is_default ? '⭐ 預設' : '' }}
                  </option>
                </select>

                <div v-if="getGroupAddressPreview(group)" class="selected_address_preview">
                  <strong>{{ getGroupAddressPreview(group).receiver_name }}</strong> / {{ getGroupAddressPreview(group).receiver_phone }}<br>
                  {{ getGroupAddressPreview(group).city }}{{ getGroupAddressPreview(group).district }}{{ getGroupAddressPreview(group).detail_address }}
                </div>

                <p v-if="savedAddresses.length === 0" style="color: #999; font-size: 0.85rem; margin-top: 10px;">
                  尚無儲存的地址，請切換至「手動填寫」或先至
                  <NuxtLink to="/member/address" style="color: #C1A96C;">地址管理</NuxtLink>
                  新增地址。
                </p>
              </div>

              <!-- 手動填寫 -->
              <div v-if="group.mode === 'manual'">
                <div class="form_row">
                  <div class="form_group">
                    <label class="form_label">收件人姓名 <span class="required">*</span></label>
                    <input v-model="group.form.receiver_name" class="form_input" placeholder="請輸入收件人姓名">
                  </div>
                  <div class="form_group">
                    <label class="form_label">聯絡電話 <span class="required">*</span></label>
                    <input v-model="group.form.receiver_phone" class="form_input" placeholder="09xx-xxx-xxx">
                  </div>
                </div>
                <div class="form_row">
                  <div class="form_group">
                    <label class="form_label">縣市 <span class="required">*</span></label>
                    <select v-model="group.form.city" class="form_select" @change="onGroupCityChange(group)">
                      <option value="">請選擇縣市</option>
                      <option v-for="city in Object.keys(taiwanCities)" :key="city" :value="city">{{ city }}</option>
                    </select>
                  </div>
                  <div class="form_group">
                    <label class="form_label">鄉鎮市區 <span class="required">*</span></label>
                    <select v-model="group.form.district" class="form_select" :disabled="!group.form.city">
                      <option value="">請選擇鄉鎮市區</option>
                      <option v-for="d in getGroupDistricts(group)" :key="d" :value="d">{{ d }}</option>
                    </select>
                  </div>
                </div>
                <div class="form_group">
                  <label class="form_label">詳細地址 <span class="required">*</span></label>
                  <input v-model="group.form.address" class="form_input" placeholder="請輸入路名、巷弄、門號、樓層">
                </div>
              </div>

              <!-- 盒數選擇器 -->
              <div class="box_allocator">
                <label class="form_label">寄送盒數 <span class="required">*</span></label>
                <div class="box_qty_control">
                  <button @click="group.boxCount = Math.max(1, group.boxCount - 1)" :disabled="group.boxCount <= 1">−</button>
                  <span class="box_qty_value">{{ group.boxCount }}</span>
                  <button @click="group.boxCount++" :disabled="group.boxCount >= getMaxBoxCount(index)">+</button>
                  <span class="box_qty_unit">盒</span>
                </div>
              </div>
            </div>

            <!-- 盒數分配狀態 + 新增地址按鈕 -->
            <div class="allocation_bar">
              <div class="allocation_status" :class="{ complete: isFullyAllocated, warning: !isFullyAllocated && totalAllocated > 0 }">
                <span v-if="isFullyAllocated">
                  ✅ 已分配 {{ totalAllocated }} / {{ totalQuantity }} 盒
                </span>
                <span v-else-if="remainingBoxes > 0">
                  ⚠️ 已分配 {{ totalAllocated }} / {{ totalQuantity }} 盒，尚餘 <strong>{{ remainingBoxes }}</strong> 盒未分配
                </span>
                <span v-else-if="remainingBoxes < 0">
                  ❌ 超出分配 {{ Math.abs(remainingBoxes) }} 盒，請調整
                </span>
              </div>
              <button
                class="add_address_btn"
                @click="addShippingGroup"
                :disabled="!canAddGroup"
                :title="canAddGroup ? '' : '需要至少 2 盒才能新增地址'"
              >
                <i class="fas fa-plus"></i> 新增寄送地址
              </button>
            </div>
          </div>

          <!-- 2. 付款方式 -->
          <div class="checkout_section">
            <div class="section_header">
              <i class="fas fa-credit-card"></i>
              <h2>付款方式</h2>
            </div>
            <div class="payment_options">
              <label class="payment_option" :class="{ selected: paymentMethod === 'credit_card' }">
                <input type="radio" v-model="paymentMethod" value="credit_card">
                <div class="payment_label">
                  <strong>💳 信用卡付款</strong>
                  <span>支援 VISA、MasterCard、JCB，線上安全付款</span>
                </div>
              </label>
              <label class="payment_option" :class="{ selected: paymentMethod === 'cod' }">
                <input type="radio" v-model="paymentMethod" value="cod">
                <div class="payment_label">
                  <strong>貨到付款</strong>
                  <span>商品送達時以現金付款給物流人員</span>
                </div>
              </label>
              <label class="payment_option" :class="{ selected: paymentMethod === 'transfer' }">
                <input type="radio" v-model="paymentMethod" value="transfer">
                <div class="payment_label">
                  <strong>銀行轉帳</strong>
                  <span>下單後將顯示匯款帳號，請於 3 日內完成轉帳</span>
                </div>
              </label>
            </div>
            <div v-if="paymentMethod === 'transfer'" class="transfer_info">
              <strong>匯款資訊將於訂單成立後顯示</strong><br>
              請於下單後 3 個工作天內完成匯款，逾期訂單將自動取消。
            </div>
            <div v-if="paymentMethod === 'credit_card'" class="transfer_info" style="border-color: #b8d4e8; background: #f0f7fc;">
              <strong>點擊「確認下單」後將跳轉至綠界安全付款頁面</strong><br>
              您的信用卡資料將由綠界科技加密處理，本站不會儲存您的卡號。
            </div>
          </div>

          <!-- 3. 備註 -->
          <div class="checkout_section">
            <div class="section_header">
              <i class="fas fa-pen"></i>
              <h2>訂單備註</h2>
            </div>
            <textarea v-model="orderNote" class="note_textarea" placeholder="有任何特殊需求嗎？例如：指定送達時段、禮盒包裝需求等（選填）"></textarea>
          </div>
        </div>

        <!-- ====== 右欄 ====== -->
        <div class="checkout_right">
          <div class="summary_card">
            <div class="summary_header">
              訂單摘要 ({{ totalQuantity }} 件商品)
            </div>
            <div class="summary_items">
              <div v-for="item in cartItems" :key="item.key" class="summary_item">
                <img :src="item.image" :alt="item.name" class="summary_item_img" @error="$event.target.src = '/placeholder.png'">
                <div class="summary_item_info">
                  <div class="summary_item_name">{{ item.name }}</div>
                  <div v-if="item.gradeName" class="summary_item_detail">{{ item.gradeName }}</div>
                  <div v-if="item.varieties && item.varieties.length" class="summary_item_detail">{{ item.varieties.map(v => v.name).join('、') }}</div>
                  <div class="summary_item_detail">x{{ item.quantity }}</div>
                </div>
                <div class="summary_item_price">{{ formatPrice(item.price * item.quantity) }}</div>
              </div>
            </div>

            <div class="coupon_section">
              <div v-if="cartStore.couponCode" class="applied_coupon">
                <div class="coupon_chip_info">
                  <span class="coupon_chip_icon">🎟️</span>
                  <span class="coupon_chip_title">{{ cartStore.discountTitle }}</span>
                </div>
                <button @click="removeCoupon" class="remove_coupon_btn">更換或移除</button>
              </div>
              <div v-else class="coupon_input_group">
                <!-- 將原本的手動輸入改為錢包選單 -->
                <select v-model="couponCodeInput" class="coupon_select" @change="applyCoupon" :disabled="isApplyingCoupon">
                  <option value="">-- 請選擇錢包內的優惠券 --</option>
                  <option v-for="c in userCoupons" :key="c.id" :value="c.coupon.code">
                    🎟️ {{ c.coupon.title }} 
                    <template v-if="c.coupon.min_spend > 0"> (滿 {{ formatPrice(c.coupon.min_spend) }} 可用)</template>
                  </option>
                </select>
              </div>
              
              <!-- 保留手動輸入代碼的彈性 -->
              <div class="manual_coupon_toggle" v-if="!cartStore.couponCode">
                <div class="manual_coupon_title">手動輸入其他代碼：</div>
                <div class="manual_coupon_box">
                  <input v-model="couponCodeInput" placeholder="輸入代碼，例如: TESTGRAPE" class="coupon_input" :disabled="isApplyingCoupon" @keyup.enter="applyCoupon" />
                  <button @click="applyCoupon" class="apply_coupon_btn" :disabled="!couponCodeInput || isApplyingCoupon">
                    {{ isApplyingCoupon ? '驗證中' : '套用' }}
                  </button>
                </div>
              </div>

              <div v-if="couponMessage.text" :class="['coupon_message', `msg_${couponMessage.type}`]">
                {{ couponMessage.text }}
              </div>
            </div>

            <div class="summary_totals">
              <div class="summary_line">
                <span>商品小計</span>
                <span>{{ formatPrice(subtotal) }}</span>
              </div>
              <div v-if="cartStore.discountAmount > 0" class="summary_line discount_line">
                <span>優惠折抵</span>
                <span class="discount_amount_text">- {{ formatPrice(cartStore.discountAmount) }}</span>
              </div>
              <div class="summary_line">
                <span>運費 ({{ activeGroups.length }} 個地址)</span>
                <span>{{ shippingFee === 0 ? '免運費' : formatPrice(shippingFee) }}</span>
              </div>
              <p v-if="totalQuantity > 0" class="package_info">
                📦 共 {{ packageInfo.total }} 件包裹，{{ packageInfo.free }} 件免運
                <span v-if="packageInfo.total - packageInfo.free > 0">、{{ packageInfo.total - packageInfo.free }} 件需付運費</span>
              </p>
            </div>
            <div class="summary_total_line">
              <span>應付總額</span>
              <span class="total_amount">{{ formatPrice(totalAmount) }}</span>
            </div>
          </div>

          <button
            class="submit_order_btn"
            :class="{ submitting: isSubmitting }"
            :disabled="!isFormValid || isSubmitting"
            @click="submitOrder"
          >
            <template v-if="isSubmitting">訂單處理中...</template>
            <template v-else-if="!isFullyAllocated">請先完成盒數分配</template>
            <template v-else>確認下單</template>
          </button>
        </div>
      </div>
    </ClientOnly>
  </div>
</template>

<style scoped>
@import '~/assets/css/checkout.css';

/* 多地址寄送專用樣式 */
.address_count_badge {
  margin-left: auto;
  background: #C1A96C;
  color: #fff;
  font-size: 0.75rem;
  padding: 3px 10px;
  border-radius: 12px;
  font-weight: 500;
}

.shipping_group {
  margin-bottom: 16px;
  padding-bottom: 16px;
}

.shipping_group.has_border {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 18px;
  background: #fefefe;
}

.shipping_group.incomplete {
  border-color: #e8a0a0;
  border-style: dashed;
  background: #fffbfb;
}

.group_incomplete_hint {
  font-size: 0.78rem;
  color: #C5374E;
  font-weight: 400;
  margin-left: 6px;
}

.group_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.group_label {
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
}

.group_remove_btn {
  background: none;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #999;
  font-size: 0.75rem;
  transition: all 0.2s;
}

.group_remove_btn:hover {
  background: #C5374E;
  border-color: #C5374E;
  color: #fff;
}

/* 盒數選擇器 */
.box_allocator {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px dashed #eee;
}

.box_qty_control {
  display: flex;
  align-items: center;
  gap: 0;
  margin-top: 6px;
}

.box_qty_control button {
  width: 36px;
  height: 36px;
  border: 1px solid #ddd;
  background: #fff;
  font-size: 1.1rem;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.box_qty_control button:first-child {
  border-radius: 4px 0 0 4px;
}

.box_qty_control button:nth-child(3) {
  border-radius: 0 4px 4px 0;
}

.box_qty_control button:hover:not(:disabled) {
  background: #f0f0f0;
}

.box_qty_control button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.box_qty_value {
  width: 50px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  font-weight: 700;
  font-size: 1.05rem;
  color: #333;
  background: #fff;
}

.box_qty_unit {
  margin-left: 8px;
  font-size: 0.9rem;
  color: #666;
}

/* 分配狀態欄 */
.allocation_bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-top: 4px;
}

.allocation_status {
  font-size: 0.88rem;
  color: #888;
}

.allocation_status.complete {
  color: #27ae60;
}

.allocation_status.warning {
  color: #e67e22;
}

.allocation_status strong {
  color: #C5374E;
}

.add_address_btn {
  background: none;
  border: 1px solid #C1A96C;
  color: #C1A96C;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.add_address_btn:hover:not(:disabled) {
  background: #C1A96C;
  color: #fff;
}

.add_address_btn:disabled {
  border-color: #ddd;
  color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .allocation_bar {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
}

/* 優惠券樣式 */
.coupon_section {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #eee;
}

.coupon_input_group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.coupon_select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  outline: none;
  background-color: white;
  cursor: pointer;
  appearance: auto;
}

.coupon_select:focus {
  border-color: #C1A96C;
}

.manual_coupon_toggle {
  margin-top: 12px;
  font-size: 0.85rem;
}

.manual_coupon_title {
  color: #666;
  margin-bottom: 6px;
}

.manual_coupon_box {
  display: flex;
  gap: 8px;
}

.coupon_input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.coupon_input:focus {
  border-color: #C1A96C;
}

.apply_coupon_btn {
  background: #C1A96C;
  color: white;
  border: none;
  padding: 0 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.apply_coupon_btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.apply_coupon_btn:hover:not(:disabled) {
  opacity: 0.9;
}

.applied_coupon {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border: 1px solid #e0ce9a;
  padding: 10px 14px;
  border-radius: 6px;
}

.coupon_chip_info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.coupon_chip_icon {
  font-size: 1.1rem;
}

.coupon_chip_title {
  font-weight: 600;
  color: #333;
}

.coupon_chip_code {
  color: #888;
  font-size: 0.85rem;
}

.remove_coupon_btn {
  background: none;
  border: none;
  color: #C5374E;
  font-size: 0.85rem;
  cursor: pointer;
  padding: 4px 8px;
}

.remove_coupon_btn:hover {
  text-decoration: underline;
}

.coupon_message {
  margin-top: 8px;
  font-size: 0.85rem;
}

.msg_success { color: #27ae60; }
.msg_error { color: #C5374E; }
.msg_info { color: #888; }

.discount_line {
  color: #C5374E;
  font-weight: 500;
}

.discount_amount_text {
  font-weight: 600;
}
</style>
