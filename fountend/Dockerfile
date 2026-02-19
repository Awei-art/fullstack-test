# ============================================
# Nuxt Frontend Dockerfile (多階段建置)
# ============================================

# --- 階段 1: 建置 ---
FROM node:20-alpine AS builder

WORKDIR /app

# 先複製 package 檔案並安裝依賴（利用 Docker 快取）
COPY package.json package-lock.json ./
RUN npm ci

# 複製所有原始碼
COPY . .

# 設定建置時的 API 位址（指向 Docker 內部的後端服務）
ENV NUXT_PUBLIC_API_BASE=http://backend:8000/api

# 建置 Nuxt 應用
RUN npm run build

# --- 階段 2: 運行 ---
FROM node:20-alpine AS runner

WORKDIR /app

# 從建置階段複製產出
COPY --from=builder /app/.output ./.output

# 開放 3000 port
EXPOSE 3000

# 啟動 Nuxt 伺服器
CMD ["node", ".output/server/index.mjs"]
