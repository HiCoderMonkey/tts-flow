# TTS-Flow Docker 部署指南

本项目提供了完整的Docker容器化部署方案，包括前端、后端、数据库和缓存服务。

## 目录结构

```
tts-flow-docker-compose/
├── docker-compose.yml          # 生产环境编排文件
├── docker-compose.dev.yml      # 开发环境编排文件
├── env.example                 # 环境变量示例
├── README.md                   # 本文件
└── data/                       # 数据持久化目录
    ├── mongodb/                # MongoDB数据
    ├── backend/                # 后端数据
    │   ├── logs/              # 日志文件
    │   └── uploads/           # 上传文件
    │   └── static/tts_wav     # tts音频数据
```

## 快速开始

### 1. 环境准备

确保您的系统已安装：
- Docker (版本 20.10+)
- Docker Compose (版本 2.0+)

### 2. 创建数据目录

```bash
# 创建数据目录
mkdir -p data/mongodb data/backend/logs data/backend/uploads data/backend/static/tts_wav

# 设置目录权限
chmod 755 data/mongodb data/backend/logs data/backend/uploads data/backend/static/tts_wav
```

### 3. 配置环境变量

```bash
# 复制环境变量文件
cp env.example .env

# 根据需要修改 .env 文件中的配置
# 注意：.env 文件会自动挂载到后端容器中
```

### 构建服务

#### 1. 修复代码格式（推荐）
```bash
# 修复前端代码格式问题
./fix-code-format.sh frontend

# 或者修复所有代码格式
./fix-code-format.sh all
```

#### 2. 生成Lock文件（推荐）
```bash
# 生成前端 pnpm-lock.yaml 文件
./generate-lockfile.sh frontend

# 或者生成所有lock文件
./generate-lockfile.sh all
```

#### 3. 构建镜像
```bash
# 普通构建
docker-compose build --no-cache

# 使用代理构建
./build-with-proxy.sh all

# 或者分别构建
docker compose build --no-cache backend \
  --build-arg https_proxy=http://192.168.60.163:7897 \
  --build-arg http_proxy=http://192.168.60.163:7897 \
  --build-arg all_proxy=socks5://192.168.60.163:7897

docker compose build --no-cache frontend \
  --build-arg https_proxy=http://192.168.60.163:7897 \
  --build-arg http_proxy=http://192.168.60.163:7897 \
  --build-arg all_proxy=socks5://192.168.60.163:7897
```

### 4. 启动服务

#### 生产环境
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 开发环境
```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 查看开发环境日志
docker-compose -f docker-compose.dev.yml logs -f
```

## 服务说明

### 前端服务 (Frontend)
- **端口**: 80 (生产) / 4000 (开发)
- **访问地址**: http://localhost
- **技术栈**: Vue 3 + Element Plus + Vite + Node.js 22.14
- **功能**: 提供Web用户界面

### 后端服务 (Backend)
- **端口**: 8000
- **访问地址**: http://localhost:8000
- **技术栈**: FastAPI + Python 3.10
- **功能**: 提供RESTful API服务

### 数据库服务 (MongoDB)
- **端口**: 27017
- **版本**: MongoDB 8.0
- **数据持久化**: ./data/mongodb
- **功能**: 存储应用数据



## 常用命令

### 服务管理
```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs [service_name]
```

### 数据管理
```bash
# 备份MongoDB数据
docker exec tts-flow-mongodb mongodump --out /data/backup

# 恢复MongoDB数据
docker exec tts-flow-mongodb mongorestore /data/backup

# 清理所有数据
docker-compose down -v
rm -rf data/*
```

### 开发调试
```bash
# 进入后端容器
docker exec -it tts-flow-backend bash

# 进入前端容器
docker exec -it tts-flow-frontend sh

# 进入数据库容器
docker exec -it tts-flow-mongodb mongosh
```

## 健康检查

所有服务都配置了健康检查：

- **MongoDB**: 每30秒检查数据库连接
- **Backend**: 每30秒检查API健康状态
- **Frontend**: 每30秒检查Web服务状态

## 数据持久化

所有重要数据都通过Docker volumes持久化到本地：

- **MongoDB数据**: `./data/mongodb`
- **后端日志**: `./data/backend/logs`
- **后端上传文件**: `./data/backend/uploads`
- **TTS音频文件**: `./data/backend/static/tts_wav`
- **环境变量文件**: `./.env` → `/app/.env`

## 网络配置

所有服务都在 `tts-flow-network` 网络中，使用子网 `172.20.0.0/16`。

## 安全配置

### 生产环境安全建议

1. **修改默认密码**:
   - MongoDB密码
   - 后端SECRET_KEY

2. **网络安全**:
   - 使用防火墙限制端口访问
   - 配置SSL/TLS证书
   - 启用HTTPS

3. **数据安全**:
   - 定期备份数据
   - 加密敏感数据
   - 限制数据目录权限

## 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :80
   netstat -tulpn | grep :8000
   ```

2. **权限问题**
   ```bash
   # 修复数据目录权限
   sudo chown -R 1000:1000 data/
   ```

3. **服务启动失败**
   ```bash
   # 查看详细日志
   docker-compose logs [service_name]
   
   # 重新构建镜像
   docker-compose build --no-cache
   ```

4. **前端构建失败（lock文件问题）**
   ```bash
   # 生成lock文件
   ./generate-lockfile.sh frontend
   
   # 重新构建前端
   docker-compose build --no-cache frontend
   ```

5. **前端构建失败（代码格式问题）**
   ```bash
   # 方法1：修复代码格式
   ./fix-code-format.sh frontend
   
   # 方法2：跳过格式检查（推荐用于生产环境）
   # Dockerfile已配置自动跳过格式检查
   
   # 重新构建前端
   docker-compose build --no-cache frontend
   ```

### 日志位置

- **应用日志**: `./data/backend/logs/`
- **Docker日志**: `docker-compose logs`
- **系统日志**: `/var/log/docker/`

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build --no-cache

# 重启服务
docker-compose up -d
```

## 联系支持

如有问题，请查看项目文档或提交Issue。 