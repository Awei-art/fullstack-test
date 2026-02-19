from django.contrib import admin
from .models import Variety, Product, ProductImage, ProductGrade
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
    #放在同一個頁面最下方
    inlines = [ProductImageInline, ProductGradeInline] # 讓詳細圖出現在同一個頁面