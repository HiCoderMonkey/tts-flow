# TTS Flow Backend

基于 FastAPI 的后端服务，提供用户认证和管理功能。

## 技术栈

- **语言**: Python 3.8+
- **Web框架**: FastAPI
- **数据库**: MongoDB
- **ORM**: Beanie (MongoDB ODM)
- **认证**: JWT
- **密码加密**: bcrypt

## 项目结构

```
backend/
├── app/
│   ├── api/           # API路由
│   │   ├── deps.py    # 依赖项
│   │   └── v1/        # API版本1
│   │       ├── auth.py    # 认证路由
│   │       └── users.py   # 用户路由
│   ├── core/          # 核心配置
│   │   ├── config.py  # 应用配置
│   │   ├── database.py # 数据库配置
│   │   └── security.py # 安全工具
│   ├── models/        # 数据模型
│   │   └── user.py    # 用户模型
│   ├── schemas/       # Pydantic模式
│   │   └── user.py    # 用户模式
│   ├── services/      # 业务逻辑
│   │   └── user_service.py # 用户服务
│   └── main.py        # 主应用
├── tests/             # 测试文件
├── requirements.txt   # 依赖包
├── env.example        # 环境变量示例
├── run.py            # 启动脚本
├── Dockerfile        # Docker配置
├── docker-compose.yml # Docker Compose配置
└── README.md         # 项目文档
```

## 快速启动

### 🚀 一键启动脚本（最简单）

我们提供了一个交互式启动脚本，支持多种启动方式：

```bash
# 给脚本添加执行权限
chmod +x start.sh

# 运行启动脚本
./start.sh
```

脚本会提供以下选项：
- 🐳 Docker Compose (推荐) - 一键启动所有服务
- 🐳 Docker 单独启动 - 分别启动 MongoDB 和 Backend  
- 🔧 本地开发 - 使用本地 Python 环境
- 📊 查看服务状态
- 🛑 停止所有服务
- 🧹 清理所有容器和数据

### 🧪 环境测试

在启动服务之前，建议先测试 Docker 环境：

```bash
# 给测试脚本添加执行权限
chmod +x test-docker.sh

# 运行环境测试
./test-docker.sh
```

测试脚本会检查：
- Docker 安装状态
- Docker Compose 安装状态
- Docker 守护进程状态
- 端口可用性
- Docker 镜像构建能力

### 🐳 使用 Docker Compose（推荐）

最简单的方式，一键启动所有服务：

```bash
# 1. 克隆项目并进入backend目录
cd backend

# 2. 启动所有服务（MongoDB + Backend）
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f backend

# 5. 停止服务
docker-compose down
```

### 🐳 使用 Docker 单独启动

#### 启动 MongoDB
```bash
# 启动 MongoDB 容器
docker run -d \
  --name tts-flow-mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:latest

# 查看 MongoDB 状态
docker ps | grep mongodb
```

#### 启动 Backend
```bash
# 构建后端镜像
docker build -t tts-flow-backend .

# 启动后端容器
docker run -d \
  --name tts-flow-backend \
  -p 8000:8000 \
  -e MONGODB_URL=mongodb://admin:password@host.docker.internal:27017 \
  -e DATABASE_NAME=tts_flow \
  -e SECRET_KEY=your-secret-key-here-change-in-production \
  -e DEBUG=True \
  tts-flow-backend

# 查看后端状态
docker ps | grep backend
```

### 🔧 本地开发环境

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

主要配置项：
- `SECRET_KEY`: JWT密钥（生产环境请使用强密钥）
- `MONGODB_URL`: MongoDB连接URL
- `DATABASE_NAME`: 数据库名称

#### 3. 启动MongoDB

确保MongoDB服务正在运行：

```bash
# macOS (使用Homebrew)
brew services start mongodb-community

# 或者使用Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### 4. 运行应用

```bash
python run.py
```

或者使用uvicorn：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker 命令参考

### Docker Compose 命令

```bash
# 启动服务
docker-compose up -d

# 启动并查看日志
docker-compose up

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 重新构建并启动
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f mongodb

# 进入容器
docker-compose exec backend bash
docker-compose exec mongodb mongosh
```

### Docker 单独命令

```bash
# 构建镜像
docker build -t tts-flow-backend .

# 运行容器
docker run -d --name tts-flow-backend -p 8000:8000 tts-flow-backend

# 查看运行中的容器
docker ps

# 查看容器日志
docker logs -f tts-flow-backend

# 停止容器
docker stop tts-flow-backend

# 删除容器
docker rm tts-flow-backend

# 进入容器
docker exec -it tts-flow-backend bash
```

## API端点

### 认证相关

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录

### 用户管理

- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me` - 更新当前用户信息
- `GET /api/v1/users/` - 获取用户列表（超级用户）
- `GET /api/v1/users/{user_id}` - 获取指定用户（超级用户）
- `PUT /api/v1/users/{user_id}` - 更新指定用户（超级用户）
- `DELETE /api/v1/users/{user_id}` - 删除用户（超级用户）

## 认证

API使用JWT Bearer Token认证。登录后获取token，在后续请求的Header中添加：

```
Authorization: Bearer <your_token>
```

## 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
# 安装black
pip install black

# 格式化代码
black app/
```

## 部署

### 生产环境配置

1. 设置 `DEBUG=False`
2. 使用强密钥作为 `SECRET_KEY`
3. 配置生产环境的MongoDB连接
4. 设置适当的CORS origins

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 许可证

MIT License 