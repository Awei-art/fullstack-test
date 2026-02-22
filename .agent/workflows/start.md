---
description: 啟動所有 Docker 服務（MySQL、Django、Nuxt、phpMyAdmin）
---
// turbo-all

## 啟動田園葡萄全端專案

1. 啟動所有服務
```bash
docker compose up -d --build
```

2. 等待 MySQL 健康檢查通過後，執行資料庫遷移
```bash
docker exec grape_shop_backend python manage.py migrate
```

3. 確認所有服務狀態
```bash
docker compose ps
```

4. 完成後提供以下服務位址：
- 前端：http://localhost:3000
- 後端 API：http://localhost:8000
- Admin 後台：http://localhost:8000/admin/
- phpMyAdmin：http://localhost:8080
