# 🍇 田園葡萄 - 全端電商專案

田園葡萄線上商店，採用前後端分離架構，使用 Docker Compose 一鍵部署。

## 📐 專案架構

```
my-fullstack-project/
├── backend/          # Django 後端 API
├── frontend/         # Nuxt 3 前端
├── docker-compose.yml
├── .env              # 環境變數（不上傳）
├── .env.example      # 環境變數範例
└── README.md
```

## 🛠 技術棧

| 層級 | 技術 |
|------|------|
| **前端** | Nuxt 3 + Vue 3 + Swiper.js |
| **後端** | Django 6.0 + Django REST Framework |
| **資料庫** | MySQL 8.0 |
| **認證** | JWT (Simple JWT) |
| **金流** | 綠界科技 ECPay |
| **部署** | Docker + Docker Compose |
| **靜態檔案** | WhiteNoise |
| **資料庫管理** | phpMyAdmin |

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
   docker exec -it grape_shop_backend python manage.py migrate
   ```

4. **建立管理員帳號**
   ```bash
   docker exec -it grape_shop_backend python manage.py createsuperuser
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
docker exec -it grape_shop_backend bash

# 執行 Django 資料庫遷移
docker exec -it grape_shop_backend python manage.py migrate

# 建立管理員帳號
docker exec -it grape_shop_backend python manage.py createsuperuser
```

## ⚙️ 環境變數

參考 `.env.example` 設定：

| 變數名稱 | 說明 | 預設值 |
|----------|------|--------|
| `MYSQL_ROOT_PASSWORD` | MySQL root 密碼 | `***REMOVED_DB_PASSWORD***` |
| `MYSQL_DATABASE` | 資料庫名稱 | `grape_shop` |
| `DB_USER` | 資料庫使用者 | `root` |

## 📁 Port 對照表

| 服務 | 容器內 Port | 本機 Port |
|------|------------|-----------|
| MySQL | 3306 | 3307 |
| Django | 8000 | 8000 |
| Nuxt | 3000 | 3000 |
| phpMyAdmin | 80 | 8080 |
