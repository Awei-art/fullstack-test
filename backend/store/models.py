from django.db import models
from django.contrib import admin

# 品種表
class Variety(models.Model):
    # 1. ID 欄位：Django 會自動幫你建立 (AutoField)，所以「不用」寫出來！
    
    # 2. 品種名稱
    name = models.CharField(max_length=100, verbose_name="品種名稱") 
    
    # 3. 顏色 (建議這之後可以改用選項 Select，目前先用文字輸入沒問題)
    color = models.CharField(max_length=50, verbose_name="顏色")    
    
    # 4. 品種介紹 
    # 使用 TextField 因為介紹文字通常比較長
    # blank=True 代表後台新增時，這個欄位可以留空不填
    description = models.TextField(blank=True, verbose_name="品種介紹") 

    # 5. 這個欄位控制這個品種現在有沒有貨
    is_active = models.BooleanField(default=True, verbose_name="是否有貨")

    def __str__(self):
        return self.name



# ---  Product (商品表) ---
class Product(models.Model):
    # 1. 商品名稱 (e.g. 三色葡萄禮盒)
    name = models.CharField(max_length=100, verbose_name="商品名稱")
    
    # 2. 價格 (使用 PositiveIntegerField 防止輸入負數)
    price = models.PositiveIntegerField(verbose_name="價格")
    
    # 3. 庫存 (預設為 0)
    stock = models.PositiveIntegerField(default=0, verbose_name="庫存數量")
    
    # 4. 是否為混合禮盒 (布林值，打勾代表是，沒勾代表否)
    is_mixed = models.BooleanField(default=False, verbose_name="是否為混合禮盒")
    
    # 預設為 1 (單品)，如果是雙色就設 2，三色就設 3
    mix_limit = models.PositiveIntegerField(default=1, verbose_name="混合口味上限")
    
    # 5. 🔥 關鍵連結：多對多關聯 (Many-to-Many)
    # 這行程式碼會自動建立「中間表」，讓您可以為一個禮盒選擇多種葡萄
    varieties = models.ManyToManyField(Variety, verbose_name="包含品種", related_name="products")

    # 6. 商品描述 (建議加上，方便前台顯示禮盒細節)
    description = models.TextField(blank=True, verbose_name="商品文案")

    # 7. 簡短說明 (用於首頁/列表頁)
    short_description = models.CharField(max_length=100, blank=True, verbose_name="列表簡述")

    # 8. 商品圖片 (建議加上，不然網頁會沒圖)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="商品圖片")

    # 9. 左上角標籤 (Badge)
    # 用來顯示圖片左上角的文字，例如：頂級精選、限量、預購
    badge = models.CharField(max_length=20, blank=True, verbose_name="左上角標籤")

    # 10. 單位類型 (Unit Type)
    # 使用下拉選單 (Choices) 讓您在後台選，避免打錯字
    UNIT_CHOICES = [
        ('catty', '台斤'), # 選項：(儲存值, 顯示文字)
        ('bunch', '串'),
    ]
    unit_type = models.CharField(
        max_length=10, 
        choices=UNIT_CHOICES, 
        default='catty', 
        verbose_name="計量單位"
    )

    # 11. 規格數值 (Value)
    # 例如：4 (台斤)、2 (串)。使用整數或浮點數
    unit_value = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        default=1, 
        verbose_name="規格數值"
    )
    # 可以在後台列表直接顯示組好的字串 (如 "4 台斤")
    @admin.display(description='規格說明')
    def get_spec_display(self):
        # 抓取對應的中文單位 (例如 'catty' -> '台斤')

        unit_display = dict(self.UNIT_CHOICES).get(self.unit_type, self.unit_type)
        # 如果是整數 (如 4.0) 就顯示 4，不然顯示 4.5
        value = int(self.unit_value) if self.unit_value % 1 == 0 else self.unit_value
        return f"{value} {unit_display}"

    def __str__(self):
        return self.name



# 規格資料表 (各等級 價格 庫存)
class ProductGrade(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='grades', # 👈 關鍵：讓我們可以用 product.grades 抓到資料
        verbose_name="所屬商品"
    )
    
    name = models.CharField(max_length=50, verbose_name="等級名稱") 
    # 例如：S級 (特級果), A級 (優選果)
    
    price = models.IntegerField(verbose_name="價格")
    # 這裡的價格會覆蓋原本商品的價格
    
    stock = models.IntegerField(default=0, verbose_name="庫存")
    # 每個等級的庫存是分開算的

    class Meta:
        verbose_name = "商品規格/等級"
        verbose_name_plural = "商品規格/等級"
        ordering = ['-price'] # 預設照價格排序

    def __str__(self):
        return f"{self.product.name} - {self.name}"





# 「詳細頁」的多張照片  
class ProductImage(models.Model):
    # 1. 關聯：把這張照片綁定到某個商品 (Product)
    # related_name='images' 很重要，這讓我們以後可以用 product.images 抓到所有照片
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="所屬商品"
    )
    
    # 2. 圖片檔案
    image = models.ImageField(upload_to='product_gallery/', verbose_name="商品圖片")
    
    # 3. (選用) 排序用，如果您想要控制照片誰前誰後
    order = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "商品更多圖片"
        ordering = ['order'] # 依照排序欄位顯示

    def __str__(self):
        return f"{self.product.name} 的圖片"


# ========================================
# 優惠券與折扣系統
# ========================================

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
            return min(int(self.discount_value), subtotal) 
        elif self.discount_type == 'percent':
            discount_ratio = (100 - self.discount_value) / 100
            return int(float(subtotal) * float(discount_ratio))
        elif self.discount_type == 'free_shipping':
            return shipping_fee
        return 0

    class Meta:
        verbose_name = "優惠券"
        verbose_name_plural = "優惠券管理"

    def __str__(self):
        return f"{self.title} ({self.code})"

from django.conf import settings

class UserCoupon(models.Model):
    """會員專屬優惠券（錢包功能）"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='coupons',
        verbose_name="持有會員"
    )
    coupon = models.ForeignKey(
        Coupon, 
        on_delete=models.CASCADE,
        related_name='user_coupons',
        verbose_name="優惠券"
    )
    
    is_used = models.BooleanField(default=False, verbose_name="是否已使用")
    used_at = models.DateTimeField(null=True, blank=True, verbose_name="使用時間")
    
    # 用字串 'Order' 作為 ForeignKey 目標，因為 Order 模型定義在下方
    order = models.ForeignKey(
        'Order', on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='used_coupons', verbose_name="套用的訂單"
    )

    class Meta:
        verbose_name = "會員優惠券"
        verbose_name_plural = "會員優惠券管理"
        unique_together = ('user', 'coupon') # 一個帳號目前對特定同一個優惠碼限領一張 (若想允許多張可拿掉這行)

    def __str__(self):
        status_text = "已使用" if self.is_used else "未使用"
        return f"[{status_text}] {self.user.username} - {self.coupon.title}"

# ========================================
# 訂單系統
# ========================================

from django.conf import settings
from django.utils import timezone

class Order(models.Model):
    """
    訂單主表：一筆訂單 = 一次結帳行為
    """
    ORDER_STATUS_CHOICES = [
        ('pending_payment', '待付款'),
        ('pending_shipment', '待出貨'),
        ('shipped', '待收貨'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', '貨到付款'),
        ('transfer', '銀行轉帳'),
        ('credit_card', '信用卡付款'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', '未付款'),
        ('paid', '已付款'),
    ]

    # 關聯會員
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="訂購會員"
    )

    # 訂單編號 (自動產生，格式：GS + 年月日 + 3位流水號，例如 GS20260302001)
    order_number = models.CharField(max_length=20, unique=True, verbose_name="訂單編號")

    # 收件資訊 (從地址簿帶入或手動填寫，永久儲存於訂單)
    receiver_name = models.CharField(max_length=100, verbose_name="收件人姓名")
    receiver_phone = models.CharField(max_length=20, verbose_name="收件人電話")
    shipping_city = models.CharField(max_length=20, verbose_name="收件縣市")
    shipping_district = models.CharField(max_length=20, verbose_name="收件鄉鎮市區")
    shipping_address = models.CharField(max_length=255, verbose_name="收件詳細地址")

    # 金額
    subtotal = models.PositiveIntegerField(verbose_name="商品小計")
    shipping_fee = models.PositiveIntegerField(default=0, verbose_name="運費")
    
    # 新增：優惠券欄位
    coupon_code = models.CharField(max_length=20, blank=True, verbose_name="使用的優惠碼")
    discount_amount = models.PositiveIntegerField(default=0, verbose_name="優惠折抵金額")
    
    total_amount = models.PositiveIntegerField(verbose_name="訂單總金額")

    # 狀態
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES,
        default='pending_payment', verbose_name="訂單狀態"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES,
        default='cod', verbose_name="付款方式"
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES,
        default='unpaid', verbose_name="付款狀態"
    )

    # 備註
    note = models.TextField(blank=True, verbose_name="訂單備註")

    # 付款重試次數（用於產生不重複的 ECPay 交易編號）
    payment_attempts = models.PositiveIntegerField(default=0, verbose_name="付款嘗試次數")

    # 時間戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="下單時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後更新時間")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "訂單"
        verbose_name_plural = "訂單管理"

    def __str__(self):
        return f"{self.order_number} - {self.receiver_name}"

    @staticmethod
    def generate_order_number():
        """
        自動產生訂單編號：GS + 年月日 + 3位流水號
        例如：GS20260302001, GS20260302002
        """
        today = timezone.now().strftime('%Y%m%d')
        prefix = f"GS{today}"

        # 查找今天已有幾筆訂單
        last_order = Order.objects.filter(
            order_number__startswith=prefix
        ).order_by('-order_number').first()

        if last_order:
            # 取出最後的流水號 +1
            last_seq = int(last_order.order_number[-3:])
            new_seq = last_seq + 1
        else:
            new_seq = 1

        return f"{prefix}{new_seq:03d}"


class OrderItem(models.Model):
    """
    訂單明細：每一筆品項（一個訂單可以有多個品項）
    使用「快照」機制：即使商品日後改名或下架，歷史訂單記錄不受影響
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name="所屬訂單"
    )

    # 商品關聯 (SET_NULL: 商品被刪除時，訂單記錄仍保留)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="商品"
    )

    # === 商品快照 (下單當下的資訊，永不改變) ===
    product_name = models.CharField(max_length=100, verbose_name="商品名稱快照")
    grade_name = models.CharField(max_length=50, blank=True, verbose_name="等級名稱快照")
    variety_names = models.CharField(max_length=255, blank=True, verbose_name="品種名稱快照")
    product_image = models.URLField(max_length=500, blank=True, verbose_name="商品圖片URL快照")

    # 金額
    unit_price = models.PositiveIntegerField(verbose_name="單價")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    item_total = models.PositiveIntegerField(verbose_name="品項小計")

    class Meta:
        verbose_name = "訂單品項"
        verbose_name_plural = "訂單品項"

    def __str__(self):
        return f"{self.order.order_number} - {self.product_name} x{self.quantity}"

# ========================================
# 網站快訊/公告 (Bulletin)
# ========================================
class Bulletin(models.Model):
    """
    首頁的快訊/公告
    """
    title = models.CharField(max_length=100, verbose_name="公告標題")
    content = models.TextField(verbose_name="公告內容")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用", help_text="取消勾選會在前台隱藏")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="排序權重", help_text="數字越大越排在前面")
    
    start_date = models.DateTimeField(blank=True, null=True, verbose_name="開始顯示時間", help_text="留空表示即刻顯示")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="結束顯示時間", help_text="留空表示永久顯示")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        ordering = ['-sort_order', '-created_at']
        verbose_name = "網站公告"
        verbose_name_plural = "網站公告管理"

    def __str__(self):
        return self.title