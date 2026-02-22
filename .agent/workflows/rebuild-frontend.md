---
description: 重建 Nuxt 前端容器（修改前端程式碼後使用）
---
// turbo-all

## 重建 Nuxt 前端

1. 重建前端容器
```bash
docker compose up -d --build frontend
```

2. 確認前端日誌是否正常
```bash
docker logs grape_shop_frontend --tail 20
```

3. 確認前端服務狀態
```bash
docker compose ps frontend
```
