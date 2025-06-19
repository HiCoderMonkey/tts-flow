# TTS Flow Backend 故障排除指南

## 🚨 常见问题及解决方案

### 1. ImportError: cannot import name '_QUERY_OPTIONS' from 'pymongo.cursor'

**问题描述：**
```
ImportError: cannot import name '_QUERY_OPTIONS' from 'pymongo.cursor'
```

**原因：**
`motor` 和 `pymongo` 版本不兼容导致的。

**解决方案：**

#### 方法1：使用安装脚本（推荐）
```bash
chmod +x install_deps.sh
./install_deps.sh
```

#### 方法2：手动修复
```bash
# 1. 卸载冲突的包
pip uninstall -y motor pymongo beanie

# 2. 按顺序安装兼容版本
pip install pymongo==4.6.0
pip install motor==3.3.2
pip install beanie==1.24.0

# 3. 安装其他依赖
pip install -r requirements.txt
```

#### 方法3：使用最新版本
```bash
# 更新到最新兼容版本
pip install --upgrade pymongo motor beanie
```

### 2. ValidationError: Field required [type=missing, input_value={}, input_type=dict]

**问题描述：**
```
ValidationError: 1 validation error for Settings
secret_key
  Field required [type=missing, input_value={}, input_type=dict]
```

**原因：**
缺少必需的 `SECRET_KEY` 环境变量。

**解决方案：**
```bash
# 1. 复制环境变量示例文件
cp env.example .env

# 2. 编辑 .env 文件，设置 SECRET_KEY
echo "SECRET_KEY=your-secret-key-here-change-in-production" >> .env
```

### 3. ConnectionError: [Errno 61] Connection refused

**问题描述：**
```
ConnectionError: [Errno 61] Connection refused
```

**原因：**
MongoDB 服务未启动。

**解决方案：**

#### 使用 Docker 启动 MongoDB
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### 使用 Docker Compose
```bash
docker-compose up -d mongodb
```

#### 本地安装 MongoDB
```bash
# macOS (使用 Homebrew)
brew services start mongodb-community

# Ubuntu/Debian
sudo systemctl start mongod
```

### 4. ModuleNotFoundError: No module named 'app'

**问题描述：**
```
ModuleNotFoundError: No module named 'app'
```

**原因：**
Python 路径问题，无法找到应用模块。

**解决方案：**
```bash
# 确保在 backend 目录下运行
cd backend

# 设置 PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 或者使用 -m 参数
python -m app.main
```

### 5. Permission denied: './start.sh'

**问题描述：**
```
Permission denied: './start.sh'
```

**原因：**
脚本文件没有执行权限。

**解决方案：**
```bash
chmod +x start.sh
chmod +x test-docker.sh
chmod +x install_deps.sh
```

### 6. Docker 相关问题

#### Docker 未安装
```bash
# macOS
brew install --cask docker

# Ubuntu
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

#### Docker 服务未启动
```bash
# macOS
open /Applications/Docker.app

# Linux
sudo systemctl start docker
```

#### 端口被占用
```bash
# 检查端口占用
lsof -i :8000
lsof -i :27017

# 停止占用端口的进程
kill -9 <PID>
```

### 7. 数据库连接问题

#### MongoDB 认证失败
```bash
# 检查连接字符串
echo $MONGODB_URL

# 测试连接
mongosh "mongodb://localhost:27017"
```

#### 数据库不存在
```bash
# 连接到 MongoDB
mongosh

# 创建数据库
use tts_flow
```

### 8. 依赖版本冲突

**解决方案：**
```bash
# 创建新的虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

## 🔍 调试技巧

### 1. 启用调试模式
```bash
# 设置环境变量
export DEBUG=True

# 或在 .env 文件中
DEBUG=True
```

### 2. 查看详细日志
```bash
# 使用 uvicorn 启动并查看日志
uvicorn app.main:app --reload --log-level debug
```

### 3. 测试数据库连接
```python
# 在 Python 中测试
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.tts_flow
print("数据库连接成功！")
```

### 4. 检查环境变量
```bash
# 查看所有环境变量
env | grep -E "(SECRET|MONGODB|DEBUG)"

# 测试配置加载
python -c "from app.core.config import settings; print(settings.dict())"
```

## 📞 获取帮助

如果以上解决方案都无法解决问题，请：

1. 检查错误日志
2. 确认系统环境（Python版本、操作系统等）
3. 提供完整的错误信息
4. 描述问题发生的具体步骤

## 🔗 相关链接

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [MongoDB 文档](https://docs.mongodb.com/)
- [Motor 文档](https://motor.readthedocs.io/)
- [Beanie 文档](https://roman-right.github.io/beanie/) 