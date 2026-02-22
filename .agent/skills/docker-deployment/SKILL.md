---
name: Docker 部署與維運
description: Docker Compose 部署、容器管理、資料庫維運、疑難排解的完整指南
---

# Docker 部署與維運指南

## 架構概覽

```
                    ┌──────────────┐
                    │   Browser    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         :3000│       :8000│       :8080│
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Nuxt 3  │ │  Django  │ │phpMyAdmin│
        │ Frontend │ │ Backend  │ │          │
        └──────────┘ └────┬─────┘ └────┬─────┘
                          │            │
                     :3306│       :3306│
                          ▼            ▼
                    ┌──────────────────┐
                    │    MySQL 8.0     │
                    │  grape_shop_db   │
                    └──────────────────┘
```

所有服務在 `grape_network` 網路中互連。

## 容器管理

### 啟動
```bash
docker compose up -d --build
```

### 停止
```bash
docker compose down
```

### 只重建特定服務
```bash
docker compose up -d --build backend    # 只重建後端
docker compose up -d --build frontend   # 只重建前端
```

### 查看日誌
```bash
docker compose logs -f              # 所有服務
docker logs grape_shop_backend -f    # 特定容器
docker logs --tail 50 grape_shop_backend  # 最近 50 行
```

### 進入容器
```bash
docker exec -it grape_shop_backend bash     # 進入後端容器
docker exec -it grape_shop_db mysql -u root -p***REMOVED_DB_PASSWORD***  # 進入 MySQL
```

## 資料庫維運

### 執行 Migration
```bash
docker exec grape_shop_backend python manage.py makemigrations
docker exec grape_shop_backend python manage.py migrate
```

### 建立 Superuser
```bash
docker exec -it grape_shop_backend python manage.py createsuperuser
```

### 備份資料庫
```bash
# 從容器內的 MySQL 匯出（推薦）
docker exec grape_shop_db mysqldump -u root -p***REMOVED_DB_PASSWORD*** --default-character-set=utf8mb4 grape_shop > backup.sql
```

### 還原資料庫
```bash
# 1. 複製檔案進容器
docker cp backup.sql grape_shop_db:/tmp/backup.sql

# 2. 重建資料庫
docker exec -i grape_shop_db mysql -u root -p***REMOVED_DB_PASSWORD*** -e "DROP DATABASE IF EXISTS grape_shop; CREATE DATABASE grape_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. 匯入
docker exec -i grape_shop_db mysql -u root -p***REMOVED_DB_PASSWORD*** --default-character-set=utf8mb4 grape_shop -e "source /tmp/backup.sql"
```

### 複製媒體檔案進容器
```bash
docker cp product_images grape_shop_backend:/app/media/product_images
docker cp product_gallery grape_shop_backend:/app/media/product_gallery
```

## 環境變數

設定在 `.env` 檔案中：

| 變數 | 說明 | 預設值 |
|------|------|--------|
| `MYSQL_ROOT_PASSWORD` | MySQL root 密碼 | `***REMOVED_DB_PASSWORD***` |
| `MYSQL_DATABASE` | 資料庫名稱 | `grape_shop` |
| `DB_USER` | 資料庫使用者 | `root` |
| `DJANGO_SECRET_KEY` | Django 密鑰 | - |
| `DJANGO_DEBUG` | Debug 模式 | `True` |

## 疑難排解

### 問題：中文亂碼（???）
**原因**：mysqldump 匯出時編碼不正確，或 PowerShell 的 `>` 重導向使用 UTF-16
**解法**：
- 匯出時加上 `--default-character-set=utf8mb4`
- 使用 `cmd /c "... > file.sql"` 而不是 PowerShell 的 `>`

### 問題：Django Admin 沒有 CSS
**原因**：Gunicorn 不會 serve 靜態檔案
**解法**：安裝 WhiteNoise（已設定）
- `requirements.txt` 加入 `whitenoise`
- `settings.py` 加入 `WhiteNoiseMiddleware`
- `settings.py` 設定 `STATICFILES_STORAGE`

### 問題：ImageField 報錯
**原因**：缺少 Pillow 套件
**解法**：`requirements.txt` 加入 `Pillow>=10.0,<11.0`

### 問題：圖片 Not Found
**原因**：媒體檔案沒有複製進 Docker 容器
**解法**：使用 `docker cp` 將本機的 `product_images/` 和 `product_gallery/` 複製進容器的 `/app/media/`

### 問題：工具指令卡住
**原因**：專案在 OneDrive 同步資料夾中
**解法**：將專案移到 `C:\Projects\` 等非 OneDrive 路徑

### 問題：mysqldump 找不到
**原因**：Laragon 的 MySQL 執行檔不在系統 PATH 中
**解法**：使用完整路徑 `C:\laragon\bin\mysql\mysql-8.4.3-winx64\bin\mysqldump.exe`

## Volume 持久化

| Volume | 掛載位置 | 用途 |
|--------|---------|------|
| `mysql_data` | `/var/lib/mysql` | MySQL 資料 |
| `backend_media` | `/app/media` | 上傳的媒體檔案 |
| `backend_static` | `/app/staticfiles` | Django 靜態檔案 |

⚠️ `docker compose down` 不會刪除 volume，資料會保留。
若要徹底清除：`docker compose down -v`。
