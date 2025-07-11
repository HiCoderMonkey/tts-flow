# 构建阶段
FROM node:22.14-alpine AS builder

# 设置工作目录
WORKDIR /app

# 支持代理设置
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}

# 关闭ESLint和Prettier检查
ENV DISABLE_ESLINT_PLUGIN=true
ENV SKIP_PRETTIER=true

# 安装pnpm
RUN npm install -g pnpm

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖（如果没有lock文件则使用普通安装）
RUN if [ -f pnpm-lock.yaml ]; then \
        pnpm install --frozen-lockfile; \
    else \
        npm install; \
    fi

# 复制源代码
COPY . .

# 构建应用（提升内存限制，跳过格式检查）
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN pnpm build:pro

# 生产阶段
FROM nginx:1.20.2


COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist-pro /opt/web