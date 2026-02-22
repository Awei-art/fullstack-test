---
description: 從 SQL 備份檔還原資料庫到 Docker MySQL
---

## 還原資料庫

⚠️ 此操作會覆蓋現有資料，請先確認備份！

1. 將備份檔複製進 Docker 容器
```bash
docker cp backup_grape_shop.sql grape_shop_db:/tmp/backup.sql
```

2. 重建資料庫
```bash
docker exec -i grape_shop_db mysql -u root -p***REMOVED_DB_PASSWORD*** -e "DROP DATABASE IF EXISTS grape_shop; CREATE DATABASE grape_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

3. 匯入備份資料
```bash
docker exec -i grape_shop_db mysql -u root -p***REMOVED_DB_PASSWORD*** --default-character-set=utf8mb4 grape_shop -e "source /tmp/backup.sql"
```

4. 確認資料表
// turbo
```bash
docker exec grape_shop_db mysql -u root -p***REMOVED_DB_PASSWORD*** -e "USE grape_shop; SHOW TABLES;"
```
