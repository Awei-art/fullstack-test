# 🍇 田園葡萄 — 全端電商專案

田園葡萄線上商店，採用前後端分離架構，使用 Docker Compose 一鍵部署。
提供葡萄禮盒、甜點商品的瀏覽、購物車、結帳、優惠券、會員系統等完整電商功能。

## 📐 專案架構

```
my-fullstack-project/
├── backend/              # Django 後端 API
│   ├── accounts/         # 會員系統 (註冊/登入/地址簿/密碼管理)
│   ├── store/            # 商店核心 (商品/訂單/優惠券/金流/公告)
│   ├── config/           # Django 設定檔
│   ├── pytest.ini        # 測試設定
│   ├── requirements.txt  # Python 套件
│   └── Dockerfile
├── frontend/             # Nuxt 3 前端
│   ├── pages/            # 頁面路由
│   ├── components/       # Vue 元件
│   ├── composables/      # 組合式 API
│   ├── stores/           # Pinia 狀態管理
│   ├── assets/           # 靜態資源
│   └── Dockerfile
├── docker-compose.yml    # Docker 服務編排
├── .env                  # 環境變數（不上傳）
├── .env.example          # 環境變數範例
└── README.md
```

## 🛠 技術棧

| 層級 | 技術 |
|------|------|
| **前端** | Nuxt 4 + Vue 3 + Pinia + Swiper.js |
| **後端** | Django 6.0 + Django REST Framework |
| **資料庫** | MySQL 8.0 |
| **認證** | JWT (Simple JWT) + Google OAuth |
| **金流** | 綠界科技 ECPay |
| **圖片儲存** | Cloudinary |
| **測試** | pytest + pytest-django + factory-boy |
| **部署** | Docker + Docker Compose |
| **靜態檔案** | WhiteNoise |
| **資料庫管理** | phpMyAdmin |

## ✨ 功能列表

### 🛒 商店功能
- 葡萄禮盒商品瀏覽（分類篩選、規格選擇、混搭禮盒）
- 甜點商品瀏覽（分類篩選、規格選擇）
- 購物車（加入/移除/數量調整）
- 結帳流程（收件資訊 → 付款方式 → 訂單確認）
- 綠界金流整合（信用卡/ATM）

### 🎟️ 優惠券系統
- 優惠碼驗證與套用
- 固定金額折扣 / 百分比折扣 / 免運費
- 最低消費門檻、使用期限、使用次數限制
- 會員領取與使用紀錄

### 👤 會員系統
- 帳號密碼註冊 / Google 第三方登入
- JWT Token 認證
- 個人資料管理
- 收件地址簿（新增/編輯/刪除/設定預設）
- 訂單查詢與詳情
- 忘記密碼 / 重設密碼

### 📰 內容管理
- 最新消息（分類瀏覽、詳情頁）
- 首頁公告輪播
- 首頁輪播圖（支援電腦版/手機版）
- 品種介紹
- 品牌介紹 / FAQ 頁面

## 🚀 快速啟動

### 前置需求
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 已安裝並啟動

### 步驟

1. **複製環境變數檔案**
   ```bash
   cp .env.example .env
   ```

2. **啟動所有服務**
   ```bash
   docker compose up -d --build
   ```

3. **執行資料庫遷移**
   ```bash
   docker compose exec backend python manage.py migrate
   ```

4. **建立管理員帳號**
   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

5. **開始使用！** 🎉

## 🌐 服務位址

| 服務 | 網址 | 說明 |
|------|------|------|
| 🖥 前端網站 | [http://localhost:3000](http://localhost:3000) | Nuxt 3 前端頁面 |
| ⚙️ 後端 API | [http://localhost:8000](http://localhost:8000) | Django REST API |
| 🔧 Admin 後台 | [http://localhost:8000/admin/](http://localhost:8000/admin/) | Django 管理介面 |
| 🗄 phpMyAdmin | [http://localhost:8080](http://localhost:8080) | 資料庫管理介面 |
| 🐬 MySQL | `localhost:3307` | 資料庫連線 |

## 📋 常用指令

```bash
# 啟動所有服務
docker compose up -d --build

# 停止所有服務
docker compose down

# 查看服務狀態
docker compose ps

# 查看即時日誌
docker compose logs -f

# 只重建後端
docker compose up -d --build backend

# 只重建前端
docker compose up -d --build frontend

# 進入後端容器
docker compose exec backend bash

# 執行 Django 資料庫遷移
docker compose exec backend python manage.py migrate

# 建立管理員帳號
docker compose exec backend python manage.py createsuperuser
```

## 🧪 測試

本專案使用 `pytest` + `pytest-django` + `factory-boy` 進行後端 API 測試，共 56 個測試案例。

```bash
# 執行全部測試（詳細模式）
docker compose exec backend pytest -v

# 只跑某一組測試
docker compose exec backend pytest store/tests.py::TestCouponAPI -v

# 只跑單一測試
docker compose exec backend pytest store/tests.py::TestCouponModel::test_有效優惠券 -v
```

### 測試涵蓋範圍

| 測試類別 | 數量 | 測試重點 |
|----------|------|----------|
| 商品 API | 6 | 列表、分類篩選、詳情、404 |
| 甜點 API | 5 | 列表、分類篩選、詳情、下架過濾 |
| 訂單 API | 6 | 權限控制、只看自己的訂單 |
| 優惠券 API | 10 | 驗證、領取、我的優惠券 |
| 會員 API | 7 | 個人資料、註冊驗證、JWT 登入 |
| 地址 API | 4 | 列表、新增、刪除 |
| 消息 API | 4 | 列表、未發佈過濾、分類 |
| 公告 API | 2 | 列表、停用過濾 |
| 品種 API | 1 | 列表 |
| 輪播圖/素材 API | 2 | 列表、啟用過濾 |
| 優惠券 Model | 8 | is_valid 邏輯、折扣計算 |

## ⚙️ 環境變數

參考 `.env.example` 設定：

| 變數名稱 | 說明 | 預設值 |
|----------|------|--------|
| `MYSQL_ROOT_PASSWORD` | MySQL root 密碼 | `***REMOVED_DB_PASSWORD***` |
| `MYSQL_DATABASE` | 資料庫名稱 | `grape_shop` |
| `DB_USER` | 資料庫使用者 | `root` |
| `DJANGO_SECRET_KEY` | Django 密鑰 | ⚠️ 請自行設定 |
| `DJANGO_DEBUG` | 開發模式 | `True` |

## 📁 Port 對照表

| 服務 | 容器內 Port | 本機 Port |
|------|------------|-----------|
| MySQL | 3306 | 3307 |
| Django | 8000 | 8000 |
| Nuxt | 3000 | 3000 |
| phpMyAdmin | 80 | 8080 |
