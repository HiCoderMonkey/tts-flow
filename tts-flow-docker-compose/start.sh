#!/bin/bash

# TTS-Flow Docker 启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    TTS-Flow Docker 启动脚本    ${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_message "Docker 环境检查通过"
}

# 创建数据目录
create_data_dirs() {
    print_message "创建数据目录..."
    
    mkdir -p data/mongodb data/backend/logs data/backend/uploads data/backend/static/tts_wav
    
    # 设置目录权限
    chmod 755 data/mongodb data/backend/logs data/backend/uploads data/backend/static/tts_wav
    
    print_message "数据目录创建完成"
}

# 检查环境变量文件
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env 文件不存在，从 env.example 复制"
        cp env.example .env
        print_message "请根据需要修改 .env 文件中的配置"
    fi
}

# 启动服务
start_services() {
    local env=${1:-"production"}
    
    print_message "启动 $env 环境服务..."
    
    if [ "$env" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml up -d
    else
        docker-compose up -d
    fi
    
    print_message "服务启动完成"
}

# 检查服务状态
check_services() {
    print_message "检查服务状态..."
    
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml ps
    else
        docker-compose ps
    fi
}

# 显示访问信息
show_access_info() {
    local env=${1:-"production"}
    
    echo ""
    print_message "服务访问信息："
    echo "----------------------------------------"
    
    if [ "$env" = "dev" ]; then
        echo "前端服务: http://localhost:4000"
        echo "后端API:  http://localhost:8000"
    else
        echo "前端服务: http://localhost"
        echo "后端API:  http://localhost:8000"
    fi
    
    echo "MongoDB:  localhost:27017"
    echo "----------------------------------------"
}

# 显示日志
show_logs() {
    local env=${1:-"production"}
    
    print_message "显示服务日志 (按 Ctrl+C 退出)..."
    
    if [ "$env" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml logs -f
    else
        docker-compose logs -f
    fi
}

# 停止服务
stop_services() {
    local env=${1:-"production"}
    
    print_message "停止 $env 环境服务..."
    
    if [ "$env" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml down
    else
        docker-compose down
    fi
    
    print_message "服务已停止"
}

# 清理服务
clean_services() {
    local env=${1:-"production"}
    
    print_warning "这将删除所有容器和数据，确定继续吗？(y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_message "清理 $env 环境服务..."
        
        if [ "$env" = "dev" ]; then
            docker-compose -f docker-compose.dev.yml down -v
        else
            docker-compose down -v
        fi
        
        rm -rf data/*
        print_message "清理完成"
    else
        print_message "取消清理操作"
    fi
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  start [env]    启动服务 (env: production|dev, 默认: production)"
    echo "  stop [env]     停止服务 (env: production|dev, 默认: production)"
    echo "  restart [env]  重启服务 (env: production|dev, 默认: production)"
    echo "  status [env]   查看服务状态 (env: production|dev, 默认: production)"
    echo "  logs [env]     查看服务日志 (env: production|dev, 默认: production)"
    echo "  clean [env]    清理所有容器和数据 (env: production|dev, 默认: production)"
    echo "  help           显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 start       启动生产环境"
    echo "  $0 start dev   启动开发环境"
    echo "  $0 logs dev    查看开发环境日志"
}

# 主函数
main() {
    print_header
    
    local action=${1:-"start"}
    local env=${2:-"production"}
    
    case $action in
        "start")
            check_docker
            create_data_dirs
            check_env_file
            start_services "$env"
            check_services "$env"
            show_access_info "$env"
            ;;
        "stop")
            stop_services "$env"
            ;;
        "restart")
            stop_services "$env"
            sleep 2
            start_services "$env"
            check_services "$env"
            ;;
        "status")
            check_services "$env"
            ;;
        "logs")
            show_logs "$env"
            ;;
        "clean")
            clean_services "$env"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "未知操作: $action"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@" 