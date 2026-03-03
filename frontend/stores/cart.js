// stores/cart.js
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    // 1. 初始一律給空陣列，確保伺服器與瀏覽器第一時間看到的一樣
    items: [],
    // 側邊小購物車的開關狀態
    isMiniCartOpen: false,

    // 優惠券資訊
    couponCode: '',
    discountTitle: '',
    discountAmount: 0,
    shippingFee: 150 // 假設固定運費, 可視需求調整
  }),

  getters: {
    // 計算購物車總金額
    totalPrice: (state) => {
      return state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
    },
    // 計算購物車總數量 (顯示在右上角小圖示用)
    totalQty: (state) => {
      return state.items.reduce((total, item) => total + item.quantity, 0)
    },
    // 計算最終應付總額
    finalTotal: (state) => {
      let calc = state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
      calc = calc - state.discountAmount + state.shippingFee
      return calc < 0 ? 0 : calc
    }
  },

  actions: {
    // 🔥 2. 新增這個動作：專門用來從瀏覽器讀取資料
    loadFromLocalStorage() {
      if (process.client) {
        console.log('CartStore: Loading from localStorage...')
        const saved = localStorage.getItem('my-cart')
        if (saved) {
          try {
            this.items = JSON.parse(saved)
            console.log('CartStore: Loaded items:', this.items)
          } catch (e) {
            console.error('CartStore: Error parsing local storage', e)
          }
        } else {
          console.log('CartStore: No items found in localStorage')
        }
      }
    },
    // 🔥 核心功能：加入購物車
    addToCart(product, silent = false) {
      // 🔥 解決品種沒選時的 .map() 報錯：加上長度判斷與預設值
      const varietiesStr = (product.varieties && product.varieties.length > 0)
        ? product.varieties.map(v => v.id).sort().join('-')
        : 'no-variety'

      const uniqueKey = `${product.id}-${product.gradeId || 'no-grade'}-${varietiesStr}`
      // 2. 檢查購物車裡面是不是已經有這個東西了？
      const existingItem = this.items.find(item => item.key === uniqueKey)

      if (existingItem) {
        // A. 如果有，就只要增加數量 (先檢查庫存上限)
        if (existingItem.quantity + product.quantity > product.maxStock) {
          if (!silent) {
            alert(`加入失敗！購物車內的數量已達庫存上限 (${product.maxStock} 件)`)
          }
          return false // 中斷加入流程並回傳失敗
        }
        existingItem.quantity += product.quantity
      } else {
        // B. 如果沒有，就推入一個新的物件，並加上 key
        this.items.push({
          key: uniqueKey, // 用來識別的鑰匙
          ...product      // 把商品的所有資訊 (圖片、名稱、價格...) 都存進去
        })
      }

      // 3. 存到瀏覽器的 LocalStorage (這樣重新整理才不會不見)
      this.saveToLocalStorage()
      return true // 回傳成功
    },

    // 移除某個商品
    removeFromCart(key) {
      this.items = this.items.filter(item => item.key !== key)
      this.saveToLocalStorage()
    },

    // 儲存 helper
    saveToLocalStorage() {
      if (process.client) {
        console.log('CartStore: Saving to localStorage...', this.items)
        localStorage.setItem('my-cart', JSON.stringify(this.items))
      }
    },

    // 控制小購物車狀態
    toggleMiniCart() {
      this.isMiniCartOpen = !this.isMiniCartOpen
    },
    openMiniCart() {
      this.isMiniCartOpen = true
    },
    closeMiniCart() {
      this.isMiniCartOpen = false
    },
    // 清空購物車（結帳成功後使用）
    clearCart() {
      this.items = []
      this.couponCode = ''
      this.discountTitle = ''
      this.discountAmount = 0
      this.saveToLocalStorage()
    },

    // 設定優惠券
    setCoupon(code, title, amount) {
      this.couponCode = code
      this.discountTitle = title
      this.discountAmount = amount
    },

    // 移除優惠券
    removeCoupon() {
      this.couponCode = ''
      this.discountTitle = ''
      this.discountAmount = 0
    }
  }
})