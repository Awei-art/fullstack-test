---
description: 備份 Docker MySQL 資料庫到本機 SQL 檔案
---
// turbo-all

## 備份 Docker MySQL 資料庫

1. 從 Docker MySQL 容器匯出資料庫
```bash
docker exec grape_shop_db mysqldump -u root -p***REMOVED_DB_PASSWORD*** --default-character-set=utf8mb4 grape_shop > backup_grape_shop.sql
```

2. 確認備份檔案已建立
```bash
Get-Item backup_grape_shop.sql | Select-Object Name, Length, LastWriteTime
```

備份檔案會儲存在專案根目錄：`backup_grape_shop.sql`
