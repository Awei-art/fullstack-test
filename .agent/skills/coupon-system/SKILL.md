---
name: 優惠券與折扣系統
description: 優惠券的資料庫結構 (Model)、前端套用邏輯、狀態判斷與結帳驗證流程
---

# 田園葡萄 優惠券與折扣系統規範

本規範定義了如何在系統中實作「優惠碼 / 優惠券」功能，以及如何與現有的結帳系統無縫整合。

## 一、優惠券主檔模型 (Coupon Model)

建議建立在 `store` 或獨立的 `promotions` App 中。

```python
class Coupon(models.Model):
    """
    優惠券規則主檔
    """
    DISCOUNT_TYPE_CHOICES = [
        ('fixed', '固定金額折抵'),
        ('percent', '百分比折扣'),
        ('free_shipping', '免運費'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="優惠碼")
    title = models.CharField(max_length=100, verbose_name="優惠名稱")
    
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name="折扣類型")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="折扣數值")
    # 若為 fixed，100 代表折 100 元
    # 若為 percent，90 代表 9 折，85 代表 85 折
    
    min_spend = models.PositiveIntegerField(default=0, verbose_name="最低消費門檻")
    
    valid_from = models.DateTimeField(verbose_name="生效時間")
    valid_to = models.DateTimeField(verbose_name="失效時間")
    
    usage_limit = models.PositiveIntegerField(default=0, verbose_name="總共可使用次數 (0表無限)")
    used_count = models.PositiveIntegerField(default=0, verbose_name="已使用次數")
    
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")

    def is_valid(self, order_subtotal):
        """檢查此優惠券目前是否可用"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False, "此優惠碼已被停用"
        if self.valid_from > now:
            return False, "此優惠碼尚未生效"
        if self.valid_to < now:
            return False, "此優惠碼已過期"
        if self.usage_limit > 0 and self.used_count >= self.usage_limit:
            return False, "此優惠碼已被兌換完畢"
        if order_subtotal < self.min_spend:
            return False, f"未達最低消費門檻 (NT$ {self.min_spend})"
            
        return True, "可使用此優惠碼"

    def calculate_discount(self, subtotal, shipping_fee=0):
        """計算折抵金額"""
        if self.discount_type == 'fixed':
            return min(self.discount_value, subtotal) # 折抵金額不能大於商品小計
        elif self.discount_type == 'percent':
            # 依賴百分比計算，90 = 打 9 折，等於折扣掉 10%
            discount_ratio = (100 - self.discount_value) / 100
            return int(float(subtotal) * discount_ratio)
        elif self.discount_type == 'free_shipping':
            return shipping_fee
        return 0
```

## 二、使用者優惠券紀錄 (UserCoupon Model) (可選，第二階段進階)

若要實作「會員錢包」，讓每個會員領取專屬優惠券並確保每人限用一次。

```python
class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    
    is_used = models.BooleanField(default=False, verbose_name="是否已使用")
    used_at = models.DateTimeField(null=True, blank=True, verbose_name="使用時間")
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="套用的訂單")
```

## 三、結帳模型更新 (Order Update)

訂單主表需要新增欄位來記錄「套用了哪張優惠券」以及「折了多少錢」。

```python
# 修改 store.models.Order
class Order(models.Model):
    # ... 原本的欄位 ...
    
    # 新增：優惠券欄位
    coupon_code = models.CharField(max_length=20, blank=True, verbose_name="使用的優惠碼")
    discount_amount = models.PositiveIntegerField(default=0, verbose_name="優惠折抵金額")
    
    # 修改總金額計算公式：
    # total_amount = subtotal - discount_amount + shipping_fee
```

## 四、結帳 API 與後端驗證邏輯

當前端呼叫 `/api/orders/` 建立訂單時，如果 Request 帶有 `coupon_code`：

1. **查找優惠碼：** `Coupon.objects.get(code=request.data['coupon_code'])`
2. **驗證有效性：** 呼叫 `coupon.is_valid(subtotal)` 檢查期限與低消。
3. **計算折扣金額：** 呼叫 `coupon.calculate_discount()`。
4. **驗證前端金額：** 後端嚴格重算 `total_amount = subtotal - discount_amount + shipping_fee`，不可相信前端傳來的 `total_amount`。
5. **扣除名額：** 若訂單建立成功，需將 `coupon.used_count += 1` 並存檔（需在 `transaction.atomic()` 內完成）。

## 五、前端整合與介面

### 5.1 結帳頁面 (Checkout)
在右側「訂單摘要」區塊加入：
- **輸入框：** 「輸入優惠代碼」與 [套用] 按鈕。
- **打 API 驗證：** 點擊套用時，發送打 `/api/coupons/validate/` API 驗證該碼是否可用及回傳折扣金額。
- **更新摘要：** 若套用成功，明細需多一行紅字顯示：`優惠折抵： - NT$ 100`。
- **建立訂單：** 按下送出訂單時，Payload 需額外帶上 `coupon_code`。

### 5.2 會員中心 (`/member/coupons`)
- 列出該會員帳戶中已綁定的優惠券（需實作 `UserCoupon` 才能達到此功能）。
- 以不同顏色區分：可用 (金色)、已過期/已使用 (灰色)。
