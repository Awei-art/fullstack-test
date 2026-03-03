---
name: 田園葡萄專案架構
description: 專案整體架構、技術棧、服務配置、目錄結構的完整參考
---

# 田園葡萄 全端電商專案架構

## 專案概述
田園葡萄是一個前後端分離的電商網站，使用 Docker Compose 進行容器化部署。
主要販售葡萄禮盒，支援多品種混搭、等級規格選購。

## 技術棧

### 前端 (frontend/)
- **框架**: Nuxt 3 (Vue 3) - 使用 Nuxt 4.3.0
- **語言**: JavaScript
- **狀態管理**: Pinia（購物車等全域狀態）
- **UI 輪播**: Swiper.js
- **圖示**: Font Awesome 6.5 (CDN)
- **CSS**: 每個 component 有對應的獨立 CSS 檔案在 `assets/css/`

### 後端 (backend/)
- **框架**: Django 6.0
- **API**: Django REST Framework 3.15
- **認證**: JWT (Simple JWT) + 社群登入 (LINE / Google OAuth)
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
│   ├── skills/                # AI 技能知識庫 (7 個)
│   └── workflows/             # 自動化工作流程 (9 個)
├── backend/                   # Django 後端
│   ├── config/                # Django 專案設定
│   │   ├── settings.py        # 主要設定檔
│   │   ├── urls.py            # 根 URL 路由
│   │   └── wsgi.py
│   ├── accounts/              # 帳號 App（使用者管理）
│   │   ├── models.py          # User, UserLoginRecord, UserAddress
│   │   ├── serializers.py     # UserSerializer, RegisterSerializer, UserAddressSerializer 等
│   │   ├── views.py           # 登入/註冊/Profile/地址/密碼變更 等 API
│   │   └── urls.py
│   ├── store/                 # 商店 App（商品管理）
│   │   ├── models.py          # Product, Variety, ProductGrade, ProductImage
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── product_images/        # 本機產品圖片（需複製進 Docker）
│   ├── product_gallery/       # 本機產品相簿（需複製進 Docker）
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                  # Nuxt 3 前端
│   ├── components/            # Vue 元件（20 個）
│   ├── pages/                 # 頁面路由（詳見下方）
│   ├── layouts/
│   │   └── default.vue        # 預設版型（Header + Footer）
│   ├── stores/                # Pinia 狀態管理
│   ├── middleware/             # 路由中間件 (auth 認證)
│   ├── assets/css/            # 元件對應 CSS 檔案
│   ├── nuxt.config.ts
│   └── Dockerfile
├── docker-compose.yml         # Docker 服務編排
├── .env                       # 環境變數（不上傳 Git）
├── .env.example               # 環境變數範例
├── .gitignore
└── README.md
```

## 前端頁面路由

| 路徑 | 檔案 | 說明 |
|------|------|------|
| `/` | `pages/index.vue` | 首頁 |
| `/login` | `pages/login/index.vue` | 登入頁（含 LoginCard 元件）|
| `/login/callback` | `pages/login/callback.vue` | LINE OAuth 回呼頁 |
| `/login/google-callback` | `pages/login/google-callback.vue` | Google OAuth 回呼頁 |
| `/register` | `pages/register.vue` | 註冊頁 |
| `/forgot-password` | `pages/forgot-password.vue` | 忘記密碼（寄送重設信）|
| `/reset-password` | `pages/reset-password.vue` | 重設密碼（驗證 Token）|
| `/products` | `pages/products/index.vue` | 商品列表頁 |
| `/products/:id` | `pages/products/[id].vue` | 商品詳情頁 |
| `/cart` | `pages/cart.vue` | 購物車頁 |
| `/faq` | `pages/faq.vue` | 常見問題頁 |
| `/member` | `pages/member/index.vue` | 會員中心首頁 |
| `/member/profile` | `pages/member/profile.vue` | 會員基本資料（暱稱/性別/生日/通知）|
| `/member/password` | `pages/member/password.vue` | 修改登入密碼（獨立頁面）|
| `/member/address` | `pages/member/address.vue` | 收件地址管理（CRUD / 預設切換動畫）|

## 前端元件清單 (20 個)

| 元件 | 說明 |
|------|------|
| `AppHeader.vue` | 全站 Header（含登入狀態/Mini 購物車）|
| `AppFooter.vue` | 全站 Footer |
| `AppBreadcrumb.vue` | 麵包屑導覽 |
| `LoginCard.vue` | 登入表單（帳號密碼 + LINE/Google 快速登入）|
| `RegisterCard.vue` | 註冊表單 |
| `MemberSidebar.vue` | 會員中心左側選單（含子選單動態 Active）|
| `MiniCart.vue` | Header 右上角的迷你購物車下拉 |
| `CartShop.vue` | 購物車完整頁面元件 |
| `ProductDetail.vue` | 商品詳情頁（品種選擇/等級/數量）|
| `ProductSalesSection.vue` | 首頁商品銷售區塊 |
| `ProductSection.vue` | 首頁商品展示區 |
| `SelectionSection.vue` | 首頁精選區 |
| `ComparisonSection.vue` | 品種比較區 |
| `IntroSection.vue` | 品牌介紹區 |
| `MediaSection.vue` | 媒體露出/合作夥伴區 |
| `DessertSection.vue` | 甜點搭配區 |
| `SaleBanner.vue` | 促銷橫幅 |
| `Bulletin.vue` | 佈告欄/公告區 |
| `FaqSection.vue` | FAQ 常見問題區 |
| `ShippingCalculator.vue` | 運費計算器 |

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

## API 路由總覽

### 認證相關 (JWT / OAuth)
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/token/` | JWT 登入（帳密換 Token，含記錄登入紀錄）|
| POST | `/api/token/refresh/` | 刷新 JWT Token |
| POST | `/api/register/` | 帳號密碼註冊 |
| POST | `/api/auth/line/` | LINE OAuth 登入 |
| POST | `/api/auth/google/` | Google OAuth 登入 |

### 會員管理
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/profile/` | 取得會員資料 |
| PUT | `/api/profile/` | 更新會員基本資料（暱稱/性別/生日/通知）|
| POST | `/api/auth/forgot-password/` | 寄送忘記密碼重設信 |
| POST | `/api/auth/reset-password/` | 驗證 Token 並重設密碼 |
| POST | `/api/auth/password/change/` | 已登入會員修改密碼（需驗證舊密碼）|

### 會員地址簿
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/address/` | 取得所有收件地址 |
| POST | `/api/address/` | 新增收件地址 |
| GET | `/api/address/<id>/` | 取得單一地址 |
| PUT | `/api/address/<id>/` | 更新地址（含切換預設）|
| DELETE | `/api/address/<id>/` | 刪除地址 |

### 商品管理
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/products/` | 取得所有商品列表 |
| GET | `/api/products/<id>/` | 取得單一商品詳情（含品種/等級/圖片）|

### Admin 後台
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/admin/` | Django Admin 管理後台 |

## 資料庫模型 (Models)

### accounts App
| 模型 | 說明 | 重要欄位 |
|------|------|---------|
| `User` | 自訂使用者 (繼承 AbstractUser) | username, email, password, nickname, gender, birth_month_day, accept_promotions, line_id, google_id, avatar, level, phone |
| `UserLoginRecord` | 登入紀錄 | user(FK), login_time, ip_address, location, device_info |
| `UserAddress` | 會員地址簿 | user(FK), title, receiver_name, receiver_phone, city, district, detail_address, is_default |

### store App
| 模型 | 說明 | 重要欄位 |
|------|------|---------|
| `Variety` | 葡萄品種 | name, color, description, is_active |
| `Product` | 商品 | name, price, stock, is_mixed, mix_limit, varieties(M2M), description, short_description, image, badge, unit_type, unit_value |
| `ProductGrade` | 商品規格/等級 | product(FK), name, price, stock |
| `ProductImage` | 商品相簿 | product(FK), image, order |

## 重要注意事項
1. **不要在 OneDrive 路徑下開發**，會導致工具執行指令卡住
2. 專案應放在 `C:\Projects\` 下面
3. 媒體檔案（product_images, product_gallery）需要手動 `docker cp` 進容器
4. 後端使用 WhiteNoise 處理靜態檔案，不需額外的 Nginx
5. 會員地址簿預設排序：is_default DESC → updated_at DESC（預設地址永遠在最前面）
6. 修改密碼 API 會判斷社群登入使用者（LINE/Google），若無可用密碼則拒絕操作
7. 前端 Cookie 名稱為 `user_info`，內含 `{ token, username, ... }`
