#!/bin/bash

# TTS-Flow 快速部署脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker环境
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装"
        exit 1
    fi
    
    print_info "Docker 环境检查通过"
}

# 创建必要目录
create_directories() {
    print_info "创建数据目录..."
    mkdir -p data/mongodb data/backend/logs data/backend/uploads data/backend/static/tts_wav
    chmod 755 data/mongodb data/backend/logs data/backend/uploads data/backend/static/tts_wav
}

# 配置环境变量
setup_environment() {
    if [ ! -f .env ]; then
        print_info "创建环境变量文件..."
        cp env.example .env
        print_warning "请修改 .env 文件中的配置"
    fi
}

# 部署生产环境
deploy_production() {
    print_info "部署生产环境..."
    docker-compose up -d
    print_info "生产环境部署完成"
}

# 部署开发环境
deploy_development() {
    print_info "部署开发环境..."
    docker-compose -f docker-compose.dev.yml up -d
    print_info "开发环境部署完成"
}

# 显示服务状态
show_status() {
    print_info "服务状态："
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml ps
    else
        docker-compose ps
    fi
}

# 显示访问信息
show_access_info() {
    echo ""
    print_info "服务访问信息："
    echo "----------------------------------------"
    if [ "$1" = "dev" ]; then
        echo "前端服务: http://localhost:4000"
        echo "后端API:  http://localhost:8000"
    else
        echo "前端服务: http://localhost"
        echo "后端API:  http://localhost:8000"
    fi
    echo "MongoDB:  localhost:27017"
    echo "----------------------------------------"
}

# 主函数
main() {
    local env=${1:-"production"}
    
    echo "=================================="
    echo "    TTS-Flow 快速部署脚本"
    echo "=================================="
    
    check_docker
    create_directories
    setup_environment
    
    if [ "$env" = "dev" ]; then
        deploy_development
        show_status "dev"
        show_access_info "dev"
    else
        deploy_production
        show_status "production"
        show_access_info "production"
    fi
}

# 显示帮助
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "用法: $0 [环境]"
    echo "环境: production (默认) 或 dev"
    echo "示例: $0 dev"
    exit 0
fi

main "$@" 