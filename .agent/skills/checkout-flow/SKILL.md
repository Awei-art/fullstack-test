---
name: 結帳流程規範
description: 購物車到結帳的完整流程規範、訂單模型設計、前端頁面規劃、付款方式與 API 設計
---

# 田園葡萄 結帳流程規範

## 一、結帳流程總覽

客人從瀏覽商品到完成訂單的完整旅程如下：

```
 瀏覽商品 → 加入購物車 → 查看購物車 → 進入結帳頁 → 確認訂單 → 完成頁面
   (1)         (2)          (3)          (4)          (5)         (6)
```

### 各步驟說明

| 步驟 | 頁面 | 說明 |
|------|------|------|
| 1. 瀏覽商品 | `/products/[id]` | 選擇品種、等級、數量 |
| 2. 加入購物車 | `MiniCart.vue` 下拉 | 點擊「加入購物車」，右上角 Mini Cart 彈出確認 |
| 3. 查看購物車 | `/cart` | 完整購物車頁面，可修改數量、刪除、查看價格 |
| 4. 進入結帳 | `/checkout` | 填寫收件資訊、選擇付款方式、確認訂單明細 |
| 5. 確認下單 | `/checkout` 提交 | 呼叫後端 API 建立訂單 |
| 6. 完成頁面 | `/checkout/success` | 顯示訂單編號、感謝語、訂單摘要 |

---

## 二、後端訂單模型設計 (Django Models)

### 2.1 Order 訂單主表

```python
class Order(models.Model):
    """
    訂單主表：一筆訂單 = 一次結帳行為
    """
    ORDER_STATUS_CHOICES = [
        ('pending', '待確認'),
        ('confirmed', '已確認'),
        ('shipping', '出貨中'),
        ('delivered', '已送達'),
        ('cancelled', '已取消'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', '貨到付款'),
        ('transfer', '銀行轉帳'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', '未付款'),
        ('paid', '已付款'),
    ]
    
    # 關聯
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='orders', verbose_name="訂購會員")
    
    # 訂單編號 (自動產生，格式：GS + 年月日 + 流水號，例如 GS20260301001)
    order_number = models.CharField(max_length=20, unique=True, verbose_name="訂單編號")
    
    # 收件資訊 (從地址簿帶入或手動填寫，儲存於訂單內作為永久記錄)
    receiver_name = models.CharField(max_length=100, verbose_name="收件人姓名")
    receiver_phone = models.CharField(max_length=20, verbose_name="收件人電話")
    shipping_city = models.CharField(max_length=20, verbose_name="收件縣市")
    shipping_district = models.CharField(max_length=20, verbose_name="收件鄉鎮市區")
    shipping_address = models.CharField(max_length=255, verbose_name="收件詳細地址")
    
    # 金額
    subtotal = models.PositiveIntegerField(verbose_name="商品小計")
    shipping_fee = models.PositiveIntegerField(default=0, verbose_name="運費")
    coupon_code = models.CharField(max_length=20, blank=True, verbose_name="使用的優惠碼")
    discount_amount = models.PositiveIntegerField(default=0, verbose_name="優惠折抵金額")
    total_amount = models.PositiveIntegerField(verbose_name="訂單總金額")
    
    # 狀態
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, 
                              default='pending', verbose_name="訂單狀態")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, 
                                       default='cod', verbose_name="付款方式")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES,
                                       default='unpaid', verbose_name="付款狀態")
    
    # 備註
    note = models.TextField(blank=True, verbose_name="訂單備註")
    
    # 時間戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="下單時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後更新時間")
```

### 2.2 OrderItem 訂單品項表

```python
class OrderItem(models.Model):
    """
    訂單明細：每一筆品項（一個訂單可以有多個品項）
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name='items', verbose_name="所屬訂單")
    
    # 商品快照（即使商品日後改名或下架，訂單記錄不受影響）
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, 
                                null=True, verbose_name="商品")
    product_name = models.CharField(max_length=100, verbose_name="商品名稱快照")
    grade_name = models.CharField(max_length=50, blank=True, verbose_name="等級名稱快照")
    variety_names = models.CharField(max_length=255, blank=True, 
                                     verbose_name="品種名稱快照")
    
    # 金額
    unit_price = models.PositiveIntegerField(verbose_name="單價")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    item_total = models.PositiveIntegerField(verbose_name="品項小計")
    
    # 商品圖片快照
    product_image = models.URLField(max_length=500, blank=True, verbose_name="商品圖片URL快照")
```

---

## 三、後端 API 設計

### 3.1 訂單相關 API

| 方法 | 路徑 | 說明 | 權限 |
|------|------|------|------|
| POST | `/api/orders/` | 建立新訂單（結帳提交）| 需登入 |
| GET | `/api/orders/` | 取得會員的所有訂單列表 | 需登入 |
| GET | `/api/orders/<order_number>/` | 取得單一訂單詳情 | 需登入 |

### 3.2 建立訂單的 Request Body 範例

```json
{
  "receiver_name": "王小明",
  "receiver_phone": "0912345678",
  "shipping_city": "台中市",
  "shipping_district": "新社區",
  "shipping_address": "中和街二段100號",
  "payment_method": "cod",
  "coupon_code": "SUMMER99",
  "note": "請在週六送達，謝謝",
  "items": [
    {
      "product_id": 3,
      "grade_id": 5,
      "variety_ids": [1, 3],
      "quantity": 2
    },
    {
      "product_id": 1,
      "grade_id": 2,
      "variety_ids": [2],
      "quantity": 1
    }
  ]
}
```

### 3.3 建立訂單的後端邏輯流程

```
1. 驗證使用者已登入
2. 驗證收件資訊完整性
3. 遍歷 items：
   a. 驗證商品是否存在、是否有庫存
   b. 取得對應等級的價格
   c. 計算品項小計 (單價 × 數量)
   d. 建立 OrderItem 快照
4. 計算商品小計 = Σ 品項小計
5. 檢查優惠券 (Coupon)：
   a. 驗證代碼是否有效、是否過期、是否達低消門檻
   b. 計算優惠折抵金額 (discount_amount)
6. 計算運費（可根據 ShippingCalculator 邏輯）
7. 計算總金額 = 小計 - 優惠折抵 + 運費
8. 產生訂單編號 (GS + 日期 + 流水號)
9. 建立 Order 記錄 (包含 coupon_code 與 discount_amount)
10. 扣除庫存 (與優惠券使用次數)
11. 回傳訂單編號與確認資訊
```

---

## 四、前端頁面規劃

### 4.1 結帳頁面 (`/checkout`) 區塊設計

結帳頁面採用**兩欄式佈局**（桌面版），手機版堆疊排列：

```
┌──────────────────────────────────────────────────┐
│                  結帳頁面 Header                    │
├────────────────────────┬─────────────────────────┤
│   左欄：填寫資訊        │    右欄：訂單摘要 (Sticky) │
│                        │                         │
│ ┌────────────────────┐ │ ┌─────────────────────┐ │
│ │ 📦 收件資訊         │ │ │  商品 1  x2  $1200  │ │
│ │ [從地址簿選取 ▼]    │ │ │  商品 2  x1  $800   │ │
│ │ 或手動填寫          │ │ │─────────────────── │ │
│ │ 姓名 / 電話         │ │ │  商品小計    $2000  │ │
│ │ 縣市 / 鄉鎮 / 地址   │ │ │  運費        $150   │ │
│ └────────────────────┘ │ │  ─────────────────  │ │
│                        │ │  應付總額    $2150  │ │
│ ┌────────────────────┐ │ └─────────────────────┘ │
│ │ 💳 付款方式         │ │                         │
│ │ ○ 貨到付款          │ │                         │
│ │ ○ 銀行轉帳          │ │                         │
│ └────────────────────┘ │                         │
│                        │                         │
│ ┌────────────────────┐ │                         │
│ │ 📝 訂單備註         │ │ ┌─────────────────────┐ │
│ │ [文字輸入區]        │ │ │ [確認下單] 按鈕      │ │
│ └────────────────────┘ │ └─────────────────────┘ │
└────────────────────────┴─────────────────────────┘
```

### 4.2 收件資訊區塊邏輯

1. **已登入會員**：
   - 自動載入該會員的「預設地址」
   - 提供「選擇其他地址」下拉選單（呼叫 `/api/address/` API）
   - 允許手動修改帶入的資訊
2. **地址欄位**：
   - 收件人姓名、聯絡電話
   - 縣市下拉、鄉鎮市區下拉（複用 `taiwanCities` 資料）
   - 詳細地址文字輸入

### 4.3 訂單摘要區塊

- 從 Pinia 購物車 Store 讀取商品資料
- 顯示每一項商品的：圖片縮圖、名稱、品種、等級、數量、小計
- 提供「輸入優惠代碼」區塊進行即時驗證折抵
- 底部顯示：商品小計、優惠折抵 (若有)、運費、應付總額
- 右欄設定為 `position: sticky`，捲動頁面時固定不動

### 4.4 訂單完成頁 (`/checkout/success`)

- 顯示綠色打勾動畫（複用已做好的 success-overlay 樣式）
- 訂單編號
- 訂單摘要（收件人、地址、金額）
- 「回到首頁」和「查看訂單」按鈕

---

## 五、付款方式

### 初期支援（Phase 1）
| 方式 | 代碼 | 說明 |
|------|------|------|
| 貨到付款 | `cod` | 宅配到府，收貨時付現金給物流人員 |
| 銀行轉帳 | `transfer` | 下單後顯示匯款帳號，會員需自行轉帳後由管理員確認 |

### 未來擴充（Phase 2）
- 信用卡線上付款（需串接金流 API，例如：綠界 ECPay、藍新 NewebPay）
- LINE Pay

---

## 六、運費計算規則

| 條件 | 運費 |
|------|------|
| 訂單金額 ≥ 免運門檻（例如 $2000） | $0（免運）|
| 訂單金額 < 免運門檻 | 固定運費（例如 $150）|
| 離島地區（澎湖/金門/連江） | 加收離島運費（例如 $250）|

> 具體金額可在後端 settings.py 或資料庫中設定，便於日後調整。

---

## 七、購物車 Pinia Store 結構

```javascript
// stores/cart.js
{
  items: [
    {
      productId: 3,
      productName: '三色葡萄禮盒',
      productImage: '/media/product_images/xxx.jpg',
      gradeId: 5,
      gradeName: 'S級 (頂級果)',
      varietyIds: [1, 3],
      varietyNames: ['巨峰', '蜜紅'],
      unitPrice: 1200,
      quantity: 2,
    }
  ],
  
  // Getters
  totalItems,      // 購物車總數量
  subtotal,        // 商品小計
  shippingFee,     // 運費
  discountAmount,  // 優惠折抵金額
  totalAmount,     // 應付總額 = 小計 - 折抵 + 運費
  
  // Actions
  addItem(),       // 加入購物車
  removeItem(),    // 移除品項
  updateQuantity(), // 修改數量
  applyCoupon(),    // 套用與驗證優惠碼
  clearCart(),      // 清空購物車
}
```

---

## 八、設計風格與元件複用

### 8.1 複用現有樣式系統
- 金色主題色：`#C1A96C`
- 表單樣式：沿用 `Member_page.css` 中的 `.form-input`, `.form-select`, `.form-label`
- 成功動畫：複用 `.success-overlay`, `.success-circle`, `.scaleUpBounce` 動畫
- 地址下拉：複用 `taiwanCities` 映射資料與聯動邏輯

### 8.2 新元件規劃
| 元件 | 說明 |
|------|------|
| `CheckoutPage.vue` | 結帳主頁面 (或直接用 `pages/checkout/index.vue`) |
| `OrderSummary.vue` | 右欄訂單摘要（Sticky）|
| `AddressSelector.vue` | 地址選擇器（從地址簿帶入 / 手動輸入切換）|
| `PaymentMethodSelector.vue` | 付款方式選擇器 |
| `CheckoutSuccess.vue` | 結帳成功頁面 |

---

## 九、安全性注意事項

1. **價格以後端為準**：前端傳送 `product_id` 和 `grade_id`，後端重新查詢價格計算，**絕對不信任前端傳來的價格**。
2. **庫存檢查**：下單時後端需二次檢查庫存，若庫存不足應回傳明確錯誤訊息。
3. **訂單建立需原子操作 (Transaction)**：使用 Django 的 `transaction.atomic()` 確保扣庫存與建立訂單同步成功或同步失敗。
4. **認證守門**：所有結帳 API 必須使用 `IsAuthenticated` 權限，未登入客人應導引至登入頁。
