---
name: 田園葡萄專案架構
description: 專案整體架構、技術棧、服務配置、目錄結構的完整參考
---

# 田園葡萄 全端電商專案架構

## 專案概述
田園葡萄是一個前後端分離的電商網站，使用 Docker Compose 進行容器化部署。

## 技術棧

### 前端 (frontend/)
- **框架**: Nuxt 3 (Vue 3)
- **語言**: TypeScript / JavaScript
- **UI 輪播**: Swiper.js
- **圖示**: Font Awesome 6.5 (CDN)
- **CSS**: 每個 component 有對應的獨立 CSS 檔案在 `assets/css/`

### 後端 (backend/)
- **框架**: Django 6.0
- **API**: Django REST Framework 3.15
- **認證**: JWT (Simple JWT)
- **跨域**: django-cors-headers
- **資料庫驅動**: mysqlclient
- **靜態檔案**: WhiteNoise
- **圖片處理**: Pillow
- **WSGI**: Gunicorn

### 基礎設施
- **資料庫**: MySQL 8.0
- **容器化**: Docker + Docker Compose
- **資料庫管理**: phpMyAdmin
- **版本控制**: Git + GitHub

## 目錄結構

```
my-fullstack-project/
├── .agent/                    # Antigravity AI 設定
│   ├── skills/                # AI 技能知識庫
│   └── workflows/             # 自動化工作流程
├── backend/                   # Django 後端
│   ├── config/                # Django 專案設定
│   │   ├── settings.py        # 主要設定檔
│   │   ├── urls.py            # 根 URL 路由
│   │   └── wsgi.py
│   ├── accounts/              # 帳號 App（使用者管理）
│   │   ├── models.py          # 自訂 User 模型
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── store/                 # 商店 App（商品管理）
│   │   ├── models.py          # Product、Variety、ProductGrade、ProductImage
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── product_images/        # 本機產品圖片（需複製進 Docker）
│   ├── product_gallery/       # 本機產品相簿（需複製進 Docker）
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                  # Nuxt 3 前端
│   ├── components/            # Vue 元件（17 個）
│   ├── pages/                 # 頁面路由
│   │   ├── index.vue          # 首頁
│   │   ├── login.vue          # 登入頁
│   │   ├── register.vue       # 註冊頁
│   │   ├── cart.vue           # 購物車
│   │   ├── faq.vue            # 常見問題
│   │   ├── member.vue         # 會員中心
│   │   └── products/          # 商品相關頁面
│   ├── layouts/
│   │   └── default.vue        # 預設版型（Header + Footer）
│   ├── assets/css/            # 元件對應 CSS 檔案
│   ├── nuxt.config.ts
│   └── Dockerfile
├── docker-compose.yml         # Docker 服務編排
├── .env                       # 環境變數（不上傳 Git）
├── .env.example               # 環境變數範例
├── .gitignore
└── README.md
```

## Docker 服務配置

| 服務 | 容器名稱 | 映像檔 | Port 對應 |
|------|---------|--------|-----------|
| MySQL | grape_shop_db | mysql:8.0 | 3307:3306 |
| phpMyAdmin | grape_shop_phpmyadmin | phpmyadmin:latest | 8080:80 |
| Django 後端 | grape_shop_backend | 自建 | 8000:8000 |
| Nuxt 前端 | grape_shop_frontend | 自建 | 3000:3000 |

## 服務存取位址
- 前端：http://localhost:3000
- 後端 API：http://localhost:8000/api/
- Admin 後台：http://localhost:8000/admin/
- phpMyAdmin：http://localhost:8080

## API 路由

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/products/` | 取得所有商品列表 |
| GET | `/api/products/<id>/` | 取得單一商品細節 |
| POST | `/api/token/` | JWT 登入（取得 token）|
| POST | `/api/token/refresh/` | 刷新 JWT token |
| GET | `/admin/` | Django Admin 管理後台 |

## 資料庫架構
- **grape_shop** 資料庫，使用 utf8mb4 編碼
- MySQL root 密碼由 `.env` 中的 `MYSQL_ROOT_PASSWORD` 控制

## 重要注意事項
1. **不要在 OneDrive 路徑下開發**，會導致工具執行指令卡住
2. 專案應放在 `C:\Projects\` 下面
3. 媒體檔案（product_images, product_gallery）需要手動 `docker cp` 進容器
4. 後端使用 WhiteNoise 處理靜態檔案，不需額外的 Nginx
