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
- 額外欄位：`level`（會員等級）、`phone`（電話）
- 設定檔中 `AUTH_USER_MODEL = 'accounts.User'`

### store App（商品管理）
- **Variety**：葡萄品種（name, color, description, is_active）
- **Product**：商品（name, price, stock, is_mixed, varieties, image 等）
- **ProductGrade**：商品等級/規格（name, price, stock），ForeignKey 到 Product
- **ProductImage**：商品詳細頁多張圖片，ForeignKey 到 Product

## 新增 API 的標準流程

### Step 1: 建立 Model（models.py）

```python
# backend/store/models.py
class NewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="名稱")
    # ... 其他欄位
    
    class Meta:
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

### Step 4: 建立 View（views.py）

```python
# backend/store/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewModel
from .serializers import NewModelSerializer

@api_view(['GET'])
def get_new_models(request):
    items = NewModel.objects.all()
    serializer = NewModelSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)
```

**規範：**
- 使用 `@api_view` 裝飾器（function-based views）
- 回傳使用 `Response(serializer.data)`
- 需要圖片 URL 時必須傳 `context={'request': request}`
- 單一資源的 view 使用 `get_object_or_404`

### Step 5: 設定 URL（urls.py）

```python
# backend/store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('new-models/', views.get_new_models, name='get_new_models'),
]
```

**規範：**
- URL 使用 kebab-case（如 `product-grades/`）
- 所有 store URL 會自動加上 `/api/` 前綴（在 config/urls.py 中設定）

### Step 6: 註冊 Admin（admin.py）

```python
# backend/store/admin.py
from django.contrib import admin
from .models import NewModel

@admin.register(NewModel)
class NewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
```

### Step 7: 重建後端容器

修改完程式碼後，需要重建容器（如果有新增 Model，重建後會自動跑 migrate）：
```bash
docker compose up -d --build backend
docker exec grape_shop_backend python manage.py makemigrations
docker exec grape_shop_backend python manage.py migrate
```

## 認證相關

- JWT Token 取得：`POST /api/token/` body: `{ "username": "...", "password": "..." }`
- JWT Token 刷新：`POST /api/token/refresh/` body: `{ "refresh": "..." }`
- Token 有效期：Access 1 天，Refresh 7 天
- 需要認證的 View 加上 `@permission_classes([IsAuthenticated])`

## 重要設定
- `CORS_ALLOWED_ORIGINS`：允許前端 `localhost:3000` 跨域請求
- `MEDIA_URL = '/media/'`：媒體檔案 URL 前綴
- `MEDIA_ROOT = BASE_DIR / 'media'`：媒體檔案儲存位置
- 圖片上傳位置：`product_images/`（主圖）、`product_gallery/`（詳細頁圖片）
