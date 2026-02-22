---
description: 快速檢查所有服務的運行狀態
---
// turbo-all

## 檢查專案狀態

1. Docker 容器狀態
```bash
docker compose ps
```

2. 確認各服務健康狀況
```bash
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
```

3. 檢查磁碟空間使用
```bash
docker system df
```
