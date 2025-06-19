#!/bin/bash

# TTS Flow Backend Docker 环境测试脚本

echo "🧪 TTS Flow Backend Docker 环境测试"
echo "===================================="

# 测试函数
test_docker() {
    echo "🔍 测试 Docker 安装..."
    if command -v docker &> /dev/null; then
        echo "✅ Docker 已安装: $(docker --version)"
    else
        echo "❌ Docker 未安装"
        return 1
    fi
}

test_docker_compose() {
    echo "🔍 测试 Docker Compose 安装..."
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose 已安装: $(docker-compose --version)"
    else
        echo "❌ Docker Compose 未安装"
        return 1
    fi
}

test_docker_daemon() {
    echo "🔍 测试 Docker 守护进程..."
    if docker info &> /dev/null; then
        echo "✅ Docker 守护进程正在运行"
    else
        echo "❌ Docker 守护进程未运行，请启动 Docker Desktop 或 Docker 服务"
        return 1
    fi
}

test_ports() {
    echo "🔍 测试端口可用性..."
    
    # 测试 8000 端口
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  端口 8000 已被占用"
    else
        echo "✅ 端口 8000 可用"
    fi
    
    # 测试 27017 端口
    if lsof -Pi :27017 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  端口 27017 已被占用"
    else
        echo "✅ 端口 27017 可用"
    fi
}

test_build() {
    echo "🔍 测试 Docker 镜像构建..."
    if docker build -t tts-flow-test . >/dev/null 2>&1; then
        echo "✅ Docker 镜像构建成功"
        # 清理测试镜像
        docker rmi tts-flow-test >/dev/null 2>&1
    else
        echo "❌ Docker 镜像构建失败"
        return 1
    fi
}

# 运行所有测试
echo ""
test_docker
docker_result=$?

echo ""
test_docker_compose
compose_result=$?

echo ""
test_docker_daemon
daemon_result=$?

echo ""
test_ports

echo ""
test_build
build_result=$?

echo ""
echo "📊 测试结果汇总:"
echo "=================="

if [ $docker_result -eq 0 ] && [ $compose_result -eq 0 ] && [ $daemon_result -eq 0 ] && [ $build_result -eq 0 ]; then
    echo "🎉 所有测试通过！Docker 环境准备就绪"
    echo ""
    echo "🚀 现在可以运行启动脚本:"
    echo "   ./start.sh"
else
    echo "⚠️  部分测试失败，请检查以下项目："
    [ $docker_result -ne 0 ] && echo "   - Docker 安装"
    [ $compose_result -ne 0 ] && echo "   - Docker Compose 安装"
    [ $daemon_result -ne 0 ] && echo "   - Docker 守护进程"
    [ $build_result -ne 0 ] && echo "   - Docker 镜像构建"
    echo ""
    echo "📖 请参考 Docker 官方文档进行安装和配置"
fi 