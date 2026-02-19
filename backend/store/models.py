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