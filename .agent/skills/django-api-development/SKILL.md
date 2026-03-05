---
name: Django API 開發規範
description: 如何在 Django 後端新增 Model、Serializer、View 和 URL 的標準流程
---

# Django API 開發規範

## 概述
本專案的 Django 後端使用 Django REST Framework (DRF) 開發 API，搭配 JWT 認證。以下是新增功能時的標準流程。

## Django Apps 結構

### accounts App（帳號管理）
- 自訂 User 模型，繼承 `AbstractUser`
- 額外欄位：`level`（會員等級）、`phone`（電話）、`nickname`、`gender`、`avatar`、`line_id`、`google_id`
- `UserLoginRecord`：登入紀錄
- `UserAddress`：會員地址簿
- 設定檔中 `AUTH_USER_MODEL = 'accounts.User'`

### store App（商品管理）
- **Variety**：葡萄品種（name, color, description, is_active, image, origin, flavor, season, sort_order）
- **Product**：商品（name, price, stock, is_mixed, mix_limit, varieties, description, short_description, image, badge, unit_type, unit_value）
- **ProductGrade**：商品等級/規格（name, price, stock），ForeignKey 到 Product
- **ProductImage**：商品詳細頁多張圖片，ForeignKey 到 Product
- **Bulletin**：網站快訊公告（content, link, is_active, order）
- **NewsCategory**：最新消息分類（name, sort_order）
- **News**：最新消息（title, summary, content, cover_image, category, is_published, is_pinned, published_date）
- **Coupon**：優惠券（code, title, discount_type, discount_value, min_spend, valid_from, valid_to, usage_limit）
- **UserCoupon**：會員優惠券紀錄（user, coupon, is_used, used_at, order）
- **Order**：訂單（order_number, user, receiver_*, shipping_*, subtotal, total_amount, status, payment_method, payment_status, coupon_code, discount_amount）
- **OrderItem**：訂單明細（order, product, product_name, grade_name, variety_names, unit_price, quantity, item_total）

## 新增 API 的標準流程

### Step 1: 建立 Model（models.py）

```python
# backend/store/models.py
class NewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="名稱")
    # ... 其他欄位
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "中文名稱"
        verbose_name_plural = "中文名稱"
    
    def __str__(self):
        return self.name
```

**命名規範：**
- 模型名稱：PascalCase（如 `ProductGrade`）
- 欄位名稱：snake_case（如 `is_active`）
- 必須加上 `verbose_name` 中文名稱
- 必須實作 `__str__` 方法
- 圖片欄位使用獨立的 `upload_to` 資料夾（如 `variety_images/`、`news_images/`、`product_images/`），避免彼此干擾

### Step 2: 建立並執行 Migration

```bash
# 在 Docker 容器內執行
docker exec grape_shop_backend python manage.py makemigrations
docker exec grape_shop_backend python manage.py migrate
```

### Step 3: 建立 Serializer（serializers.py）

```python
# backend/store/serializers.py
from rest_framework import serializers
from .models import NewModel

class NewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewModel
        fields = ['id', 'name']  # 明確列出欄位，不用 '__all__'
```

**規範：**
- 使用 `ModelSerializer`
- 明確列出 `fields`，避免使用 `'__all__'`
- 圖片欄位使用 `SerializerMethodField` 搭配 `request.build_absolute_uri()` 取得完整 URL
- 關聯資料使用巢狀 Serializer
- 同一 Model 可建立多個 Serializer（如 `NewsListSerializer` 列表用精簡版 / `NewsDetailSerializer` 單篇用完整版）

### Step 4: 建立 View（views.py）

**方式 A：Function-Based View（簡單查詢）**
```python
@api_view(['GET'])
def get_new_models(request):
    items = NewModel.objects.all()
    serializer = NewModelSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)
```

**方式 B：Class-Based Generic View（推薦，新功能已採用此方式）**
```python
from rest_framework import generics
from rest_framework.permissions import AllowAny

class NewModelListView(generics.ListAPIView):
    """GET /api/new-models/ — 取得列表"""
    serializer_class = NewModelSerializer
    permission_classes = [AllowAny]
    queryset = NewModel.objects.filter(is_active=True)
```

**規範：**
- 公開性 API（如查商品、查消息）使用 `AllowAny`
- 會員性 API（如訂單、優惠券）使用 `IsAuthenticated`
- 需要圖片 URL 時必須傳 `context={'request': request}`
- 單一資源的 view 使用 `get_object_or_404` 或 `generics.RetrieveAPIView`
- 支援 GET 參數篩選時，覆寫 `get_queryset()` 方法

### Step 5: 設定 URL（urls.py）

```python
# backend/store/urls.py
from django.urls import path
from . import views
from .views import NewModelListView

urlpatterns = [
    path('new-models/', NewModelListView.as_view(), name='new-model-list'),
]
```

**規範：**
- URL 使用 kebab-case（如 `product-grades/`）
- 所有 store URL 會自動加上 `/api/` 前綴（在 config/urls.py 中設定）
- CBV 使用 `.as_view()` 綁定

### Step 6: 註冊 Admin（admin.py）

```python
# backend/store/admin.py
from django.contrib import admin
from .models import NewModel

@admin.register(NewModel)
class NewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('name',)
    search_fields = ('name',)
```

### Step 7: 重建後端容器

修改完程式碼後，需要重建容器（如果有新增 Model，重建後會自動跑 migrate）：
```bash
docker compose up -d --build backend
docker exec grape_shop_backend python manage.py makemigrations
docker exec grape_shop_backend python manage.py migrate
```

如果只改了 views / serializers / urls（沒改 Model），可以直接重啟：
```bash
docker compose restart backend
```

## 認證相關

- JWT Token 取得：`POST /api/token/` body: `{ "username": "...", "password": "..." }`
- JWT Token 刷新：`POST /api/token/refresh/` body: `{ "refresh": "..." }`
- Token 有效期：Access 1 天，Refresh 7 天
- 需要認證的 View 加上 `permission_classes = [IsAuthenticated]`

## 重要設定
- `CORS_ALLOWED_ORIGINS`：允許前端 `localhost:3000` 跨域請求
- `MEDIA_URL = '/media/'`：媒體檔案 URL 前綴
- `MEDIA_ROOT = BASE_DIR / 'media'`：媒體檔案儲存位置
- 圖片上傳位置分類：`product_images/`（商品主圖）、`product_gallery/`（商品相簿）、`variety_images/`（品種圖）、`news_images/`（消息封面）
