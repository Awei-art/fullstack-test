---
description: 重建 Django 後端容器（修改 requirements.txt 或 Dockerfile 後使用）
---
// turbo-all

## 重建 Django 後端

1. 重建後端容器
```bash
docker compose up -d --build backend
```

2. 執行資料庫遷移
```bash
docker exec grape_shop_backend python manage.py migrate
```

3. 收集靜態檔案
```bash
docker exec grape_shop_backend python manage.py collectstatic --noinput
```

4. 確認後端日誌是否正常
```bash
docker logs grape_shop_backend --tail 20
```
