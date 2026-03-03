from django.contrib import admin
from .models import Variety, Product, ProductImage, ProductGrade, Order, OrderItem, Coupon, UserCoupon, Bulletin
# Register your models here.

#定義品種頁 顯示有貨
@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    # 1. 把您想看的欄位列出來 (is_active 一定要放進來)
    list_display = ('name', 'is_active') 
    
    # 2. 設定這個欄位可以直接在列表上編輯
    # 注意：這裡只能放 list_display 裡面有的欄位
    list_editable = ('is_active',) 

    # (選用) 讓 id 或 name 可以點擊進入詳細頁
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
    list_display = ('name', 'price', 'stock', 'is_mixed', 'get_spec_display', 'mix_limit') # 列表頁顯示這幾欄
    list_editable = ('mix_limit',) # 👈 讓您可以直接在列表改數字，不用點進去
    filter_horizontal = ('varieties',) # ✨ 讓選擇品種時變成好用的左右選單
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