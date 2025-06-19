#!/bin/bash

# TTS Flow Backend 启动脚本

echo "🚀 TTS Flow Backend 启动脚本"
echo "================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请先安装 docker-compose"
    exit 1
fi

echo "请选择启动方式："
echo "1) 🐳 Docker Compose (推荐) - 一键启动所有服务"
echo "2) 🐳 Docker 单独启动 - 分别启动 MongoDB 和 Backend"
echo "3) 🔧 本地开发 - 使用本地 Python 环境"
echo "4) 📊 查看服务状态"
echo "5) 🛑 停止所有服务"
echo "6) 🧹 清理所有容器和数据"

read -p "请输入选项 (1-6): " choice

case $choice in
    1)
        echo "🐳 使用 Docker Compose 启动服务..."
        docker-compose up -d
        echo "✅ 服务启动完成！"
        echo "📊 查看服务状态: docker-compose ps"
        echo "📝 查看日志: docker-compose logs -f backend"
        echo "🌐 API文档: http://localhost:8000/docs"
        ;;
    2)
        echo "🐳 使用 Docker 单独启动服务..."
        
        # 启动 MongoDB
        echo "📦 启动 MongoDB..."
        docker run -d \
            --name tts-flow-mongodb \
            -p 27017:27017 \
            -e MONGO_INITDB_ROOT_USERNAME=admin \
            -e MONGO_INITDB_ROOT_PASSWORD=password \
            -v mongodb_data:/data/db \
            mongo:latest
        
        # 等待 MongoDB 启动
        echo "⏳ 等待 MongoDB 启动..."
        sleep 5
        
        # 构建并启动 Backend
        echo "🔨 构建后端镜像..."
        docker build -t tts-flow-backend .
        
        echo "🚀 启动后端服务..."
        docker run -d \
            --name tts-flow-backend \
            -p 8000:8000 \
            -e MONGODB_URL=mongodb://admin:password@host.docker.internal:27017 \
            -e DATABASE_NAME=tts_flow \
            -e SECRET_KEY=your-secret-key-here-change-in-production \
            -e DEBUG=True \
            tts-flow-backend
        
        echo "✅ 服务启动完成！"
        echo "📊 查看服务状态: docker ps | grep tts-flow"
        echo "🌐 API文档: http://localhost:8000/docs"
        ;;
    3)
        echo "🔧 本地开发环境启动..."
        
        # 检查Python环境
        if ! command -v python &> /dev/null; then
            echo "❌ Python 未安装，请先安装 Python"
            exit 1
        fi
        
        # 检查.env文件
        if [ ! -f .env ]; then
            echo "📝 创建 .env 文件..."
            cp env.example .env
            echo "⚠️  请编辑 .env 文件，设置 SECRET_KEY 等配置"
        fi
        
        # 安装依赖
        echo "📦 安装 Python 依赖..."
        pip install -r requirements.txt
        
        # 启动MongoDB（如果本地没有运行）
        if ! docker ps | grep -q mongodb; then
            echo "🐳 启动本地 MongoDB..."
            docker run -d -p 27017:27017 --name mongodb mongo:latest
            sleep 3
        fi
        
        echo "🚀 启动后端服务..."
        python run.py
        ;;
    4)
        echo "📊 查看服务状态..."
        echo "Docker Compose 服务:"
        docker-compose ps
        echo ""
        echo "Docker 容器:"
        docker ps | grep tts-flow
        ;;
    5)
        echo "🛑 停止所有服务..."
        docker-compose down
        docker stop tts-flow-backend tts-flow-mongodb 2>/dev/null || true
        echo "✅ 服务已停止"
        ;;
    6)
        echo "🧹 清理所有容器和数据..."
        docker-compose down -v
        docker stop tts-flow-backend tts-flow-mongodb 2>/dev/null || true
        docker rm tts-flow-backend tts-flow-mongodb 2>/dev/null || true
        docker volume rm mongodb_data 2>/dev/null || true
        echo "✅ 清理完成"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac 