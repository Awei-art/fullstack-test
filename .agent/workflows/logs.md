---
description: 查看各服務的日誌（可指定服務名稱）
---
// turbo-all

## 查看服務日誌

1. 查看所有服務最近的日誌
```bash
docker compose logs --tail 30
```

如果需要查看特定服務的日誌，可以使用：
- 後端：`docker logs grape_shop_backend --tail 30`
- 前端：`docker logs grape_shop_frontend --tail 30`
- 資料庫：`docker logs grape_shop_db --tail 30`
- phpMyAdmin：`docker logs grape_shop_phpmyadmin --tail 30`
