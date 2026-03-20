from django.contrib import admin
from .models import Variety, Product, ProductImage, ProductGrade, Order, OrderItem, Coupon, UserCoupon, Bulletin, NewsCategory, News, DessertCategory, Dessert, ProductCategory, DessertGrade, DessertImage, Banner, SiteImage
# Register your models here.

#定義品種頁 顯示有貨
@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'origin', 'season', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    list_display_links = ('name',)
    search_fields = ('name', 'origin', 'flavor')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    list_display_links = ('name',)


#產品詳細圖
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # 預設顯示 1 格空的讓您填 (不夠可以按 + 號)
    fields = ['image', 'order'] # 只顯示圖片和排序欄位
    

# 1. 等級表內嵌介面 (讓您可以在商品頁直接加等級)
class ProductGradeInline(admin.TabularInline):
    model = ProductGrade
    extra = 1 # 預設顯示 1 個空格
    fields = ['name', 'price', 'stock']



# 這裡用一個比較進階的寫法，讓您在列表就能看到價格和庫存
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_mixed', 'get_spec_display', 'mix_limit')
    list_editable = ('mix_limit',)
    list_filter = ('category',)
    search_fields = ('name',)
    filter_horizontal = ('varieties',) # ✨ 讓選擇品種時變成好用的左右選單
    #放在同一個頁面最下方
    inlines = [ProductImageInline, ProductGradeInline] # 讓詳細圖出現在同一個頁面


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'discount_type', 'discount_value', 'is_active', 'valid_to')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code', 'title')

@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'is_used', 'used_at', 'order')
    list_filter = ('is_used', 'coupon')
    search_fields = ('user__username', 'coupon__code', 'coupon__title')
    readonly_fields = ('used_at', 'order')

# ========================================
# 訂單管理 Admin
# ========================================

class OrderItemInline(admin.TabularInline):
    """訂單品項內嵌在訂單頁面"""
    model = OrderItem
    extra = 0  # 不顯示空白列
    readonly_fields = ['product_name', 'grade_name', 'variety_names', 'unit_price', 'quantity', 'item_total']
    fields = ['product_name', 'grade_name', 'variety_names', 'unit_price', 'quantity', 'item_total']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'receiver_name', 'total_amount',
        'status', 'payment_method', 'payment_status', 'created_at', 'coupon_code'
    ]
    list_filter = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields = ['order_number', 'receiver_name', 'receiver_phone', 'coupon_code']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['order_number', 'user', 'subtotal', 'shipping_fee', 'coupon_code', 'discount_amount', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    # 按下單時間排序
    ordering = ['-created_at']

@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'sort_order', 'start_date', 'end_date', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    list_editable = ('is_active', 'sort_order')
    ordering = ('-sort_order', '-created_at')


# ========================================
# 最新消息管理 Admin
# ========================================

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')
    list_editable = ('sort_order',)
    search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_pinned', 'published_date', 'is_published', 'created_at')
    list_filter = ('is_published', 'is_pinned', 'category', 'published_date')
    search_fields = ('title', 'summary', 'content')
    list_editable = ('is_published', 'is_pinned')
    ordering = ('-is_pinned', '-published_date', '-created_at')


# ========================================
# 甄點管理
# ========================================

@admin.register(DessertCategory)
class DessertCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    list_display_links = ('name',)

class DessertGradeInline(admin.TabularInline):
    model = DessertGrade
    extra = 1

class DessertImageInline(admin.TabularInline):
    model = DessertImage
    extra = 1
    fields = ['image', 'order']

@admin.register(Dessert)
class DessertAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'flavor', 'price', 'stock', 'is_active', 'sort_order')
    list_filter = ('category', 'is_active')
    list_editable = ('price', 'stock', 'is_active', 'sort_order')
    list_display_links = ('name',)
    search_fields = ('name', 'flavor')
    inlines = [DessertImageInline, DessertGradeInline]


# ========================================
# 首頁橫幅管理 Banner
# ========================================

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    ordering = ('order', '-id')
    autocomplete_fields = ('target_product', 'target_dessert')
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('title', 'subtitle', 'image', 'mobile_image', 'is_active', 'order')
        }),
        ('跳轉連結設定 (三選一)', {
            'fields': ('target_product', 'target_dessert', 'custom_link'),
            'description': '請選擇您想跳轉的目的地。若有選擇一般/甄點商品，會優先跳轉到該商品頁！'
        }),
    )


# ========================================
# 網站素材庫管理
# ========================================
from django.utils.html import format_html

@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('key', 'label', 'group', 'image_preview', 'updated_at')
    list_filter = ('group',)
    search_fields = ('key', 'label')
    list_display_links = ('key',)
    readonly_fields = ('image_preview_large', 'updated_at')
    autocomplete_fields = ('target_product', 'target_dessert')

    fieldsets = (
        ('基本資訊', {
            'fields': ('key', 'label', 'group', 'image', 'alt_text', 'image_preview_large', 'updated_at')
        }),
        ('搭配文字 (選填)', {
            'fields': ('title', 'description'),
            'classes': ('collapse',),
            'description': '標題/說明文字用於安心農產等區塊。留空則使用預設值。'
        }),
        ('跳轉設定 (選填，四選一，由上往下優先)', {
            'fields': ('target_product', 'target_dessert', 'link_page', 'custom_link'),
            'classes': ('collapse',),
            'description': '① 推薦商品 → ② 推薦甜點 → ③ 站內頁面 → ④ 自訂網址。只要填一個即可，系統會依照優先順序處理。'
        }),
    )

    @admin.display(description='預覽')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px;" />', obj.image.url)
        return '-'

    @admin.display(description='目前圖片')
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px; border-radius:8px;" />', obj.image.url)
        return '尚未上傳圖片'