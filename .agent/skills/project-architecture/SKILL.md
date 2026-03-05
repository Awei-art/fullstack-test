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
- **CSS**: 每個 component 有對應的獨立 CSS 檔案在 `assets/css/`，使用 `<style src="..." scoped>` 引入

### 後端 (backend/)
- **框架**: Django 6.0
- **API**: Django REST Framework 3.15
- **認證**: JWT (Simple JWT) + 社群登入 (LINE / Google OAuth)
- **跨域**: django-cors-headers
- **資料庫驅動**: mysqlclient
- **靜態檔案**: WhiteNoise
- **圖片處理**: Pillow
- **金流**: ECPay 綠界支付
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
│   ├── skills/                # AI 技能知識庫 (8 個)
│   └── workflows/             # 自動化工作流程 (9 個)
├── backend/                   # Django 後端
│   ├── config/                # Django 專案設定
│   │   ├── settings.py        # 主要設定檔
│   │   ├── urls.py            # 根 URL 路由
│   │   └── wsgi.py
│   ├── accounts/              # 帳號 App（使用者管理）
│   │   ├── models.py          # User, UserLoginRecord, UserAddress
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── store/                 # 商店 App（商品+訂單+內容管理）
│   │   ├── models.py          # Product, Variety, Order, News, Coupon 等
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── ecpay.py           # 綠界支付整合
│   ├── media/                 # 上傳的媒體檔案（Docker Volume）
│   │   ├── product_images/    # 商品主圖
│   │   ├── product_gallery/   # 商品相簿
│   │   ├── variety_images/    # 品種介紹圖
│   │   └── news_images/       # 最新消息封面
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                  # Nuxt 3 前端
│   ├── components/            # Vue 元件
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
| `/login` | `pages/login/index.vue` | 登入頁 |
| `/login/callback` | `pages/login/callback.vue` | LINE OAuth 回呼 |
| `/login/google-callback` | `pages/login/google-callback.vue` | Google OAuth 回呼 |
| `/login/line-callback` | `pages/login/line-callback.vue` | LINE OAuth 回呼 |
| `/register` | `pages/register.vue` | 註冊頁 |
| `/forgot-password` | `pages/forgot-password.vue` | 忘記密碼 |
| `/reset-password` | `pages/reset-password.vue` | 重設密碼 |
| `/products` | `pages/products/index.vue` | 商品列表頁 |
| `/products/:id` | `pages/products/[id].vue` | 商品詳情頁 |
| `/cart` | `pages/cart.vue` | 購物車頁 |
| `/checkout` | `pages/checkout/index.vue` | 結帳頁 |
| `/checkout/success` | `pages/checkout/success.vue` | 結帳成功頁 |
| `/checkout/ecpay-return` | `pages/checkout/ecpay-return.vue` | ECPay 回傳頁 |
| `/news` | `pages/news/index.vue` | 最新消息列表頁 |
| `/news/:id` | `pages/news/[id].vue` | 最新消息詳情頁 |
| `/about` | `pages/about.vue` | 關於田原（靜態頁面） |
| `/varieties` | `pages/varieties.vue` | 品種介紹頁 |
| `/faq` | `pages/faq.vue` | 常見問題頁 |
| `/member` | `pages/member/index.vue` | 會員中心首頁 |
| `/member/profile` | `pages/member/profile.vue` | 會員基本資料 |
| `/member/password` | `pages/member/password.vue` | 修改密碼 |
| `/member/address` | `pages/member/address.vue` | 收件地址管理 |
| `/member/orders` | `pages/member/orders.vue` | 訂單管理 |
| `/member/coupons` | `pages/member/coupons.vue` | 我的優惠券 |

## 前端元件清單

| 元件 | 說明 | CSS 檔案 |
|------|------|---------|
| `AppHeader.vue` | 全站 Header（含登入/Mini 購物車/導覽列） | `header.css` |
| `AppFooter.vue` | 全站 Footer | `footer.css` |
| `AppBreadcrumb.vue` | 麵包屑導覽 | - |
| `SaleBanner.vue` | 首頁促銷橫幅 | `sale_banner.css` |
| `IntroSection.vue` | 品牌介紹輪播 | `IntroSection.css` |
| `Bulletin.vue` | 首頁跑馬燈公告 | `Bulletin.css` |
| `ProductSection.vue` | 首頁商品展示 | `ProductSection.css` |
| `SelectionSection.vue` | 首頁精選系列 | `SelectionSection.css` |
| `ComparisonSection.vue` | 品種比較區 | `ComparisonSection.css` |
| `DessertSection.vue` | 甜點搭配區 | `DessertSection.css` |
| `MediaSection.vue` | 媒體露出區 | `MediaSection.css` |
| `ProductDetail.vue` | 商品詳情頁（品種/等級/數量） | `ProductDetail.css` |
| `ProductSalesSection.vue` | 商品銷售列表區 | `ProductSalesSection.css` |
| `LoginCard.vue` | 登入表單 | `LoginCard.css` |
| `RegisterCard.vue` | 註冊表單 | `RegisterCard.css` |
| `MiniCart.vue` | Header 迷你購物車下拉 | - |
| `CartShop.vue` | 購物車完整頁面 | - |
| `FaqSection.vue` | FAQ 手風琴問答 | `FaqSection.css` |
| `MemberSidebar.vue` | 會員中心側邊選單 | `MemberSidebar.css` |
| `ShippingCalculator.vue` | 運費計算器 | - |

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
| POST | `/api/token/` | JWT 登入 |
| POST | `/api/token/refresh/` | 刷新 JWT Token |
| POST | `/api/register/` | 帳號密碼註冊 |
| POST | `/api/auth/line/` | LINE OAuth 登入 |
| POST | `/api/auth/google/` | Google OAuth 登入 |

### 會員管理
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET/PUT | `/api/profile/` | 取得/更新會員資料 |
| POST | `/api/auth/forgot-password/` | 寄送重設信 |
| POST | `/api/auth/reset-password/` | 重設密碼 |
| POST | `/api/auth/password/change/` | 修改密碼 |

### 會員地址簿
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET/POST | `/api/address/` | 取得/新增地址 |
| GET/PUT/DELETE | `/api/address/<id>/` | 單一地址 CRUD |

### 商品管理
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/products/` | 商品列表 |
| GET | `/api/products/<id>/` | 商品詳情 |

### 品種介紹
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/varieties/` | 所有有貨品種完整資料 |

### 網站公告
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/bulletins/` | 跑馬燈公告列表 |

### 最新消息
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/news/categories/` | 消息分類列表 |
| GET | `/api/news/` | 消息列表（支援 `?category=ID` 篩選） |
| GET | `/api/news/<id>/` | 單篇消息詳情 |

### 訂單管理
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/orders/` | 建立新訂單 |
| GET | `/api/orders/` | 會員訂單列表 |
| GET | `/api/orders/<order_number>/` | 訂單詳情 |

### 優惠券
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/coupons/validate/` | 驗證優惠碼 |
| GET | `/api/coupons/my/` | 我的優惠券列表 |
| POST | `/api/coupons/claim/` | 領取優惠券 |

### 金流 (ECPay)
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/payment/repay/<order_number>/` | 重新付款 |
| POST | `/api/payment/notify/` | ECPay 背景通知 |
| POST | `/api/payment/result/` | ECPay 付款結果 |
| GET | `/api/payment/return/<order_number>/` | 前端付款回傳 |

## 資料庫模型 (Models)

### accounts App
| 模型 | 說明 | 重要欄位 |
|------|------|---------|
| `User` | 自訂使用者 | username, email, nickname, gender, birth_month_day, accept_promotions, line_id, google_id, avatar, level, phone |
| `UserLoginRecord` | 登入紀錄 | user(FK), login_time, ip_address, location, device_info |
| `UserAddress` | 地址簿 | user(FK), title, receiver_name, receiver_phone, city, district, detail_address, is_default |

### store App
| 模型 | 說明 | 重要欄位 |
|------|------|---------|
| `Variety` | 葡萄品種 | name, color, description, is_active, image, origin, flavor, season, sort_order |
| `Product` | 商品 | name, price, stock, is_mixed, mix_limit, varieties(M2M), image, badge, unit_type |
| `ProductGrade` | 商品規格 | product(FK), name, price, stock |
| `ProductImage` | 商品相簿 | product(FK), image, order |
| `Bulletin` | 網站快訊 | content, link, is_active, order |
| `NewsCategory` | 消息分類 | name, sort_order |
| `News` | 最新消息 | title, summary, content, cover_image, category(FK), is_published, is_pinned, published_date |
| `Coupon` | 優惠券 | code, title, discount_type, discount_value, min_spend, valid_from, valid_to, usage_limit |
| `UserCoupon` | 會員優惠券 | user(FK), coupon(FK), is_used, used_at, order(FK) |
| `Order` | 訂單 | order_number, user(FK), receiver_*, shipping_*, subtotal, total_amount, status, payment_method, payment_status |
| `OrderItem` | 訂單明細 | order(FK), product(FK), product_name, grade_name, variety_names, unit_price, quantity, item_total |

## 重要注意事項
1. **不要在 OneDrive 路徑下開發**，會導致工具執行指令卡住
2. 專案應放在 `C:\Projects\` 下面
3. 媒體檔案（product_images, product_gallery）需要手動 `docker cp` 進容器
4. 後端使用 WhiteNoise 處理靜態檔案，不需額外的 Nginx
5. 前端 API 連線使用 `apiBase`（SSR 用，指向 `http://backend:8000/api`）和 `apiBaseClient`（客戶端用，指向 `http://localhost:8000/api`）雙模式
6. 前端 Cookie 名稱為 `user_info`，內含 `{ token, username, ... }`
7. 圖片上傳路徑分類：`product_images/`、`product_gallery/`、`variety_images/`、`news_images/` 互不干擾
