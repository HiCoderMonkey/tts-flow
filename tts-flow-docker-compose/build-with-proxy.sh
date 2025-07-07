#!/bin/bash

# TTS-Flow 代理构建脚本

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

# 默认代理配置
DEFAULT_HTTP_PROXY="http://192.168.60.136:7897"
DEFAULT_HTTPS_PROXY="http://192.168.60.136:7897"
DEFAULT_NO_PROXY="localhost,127.0.0.1,192.168.60.136"

# 获取代理配置
get_proxy_config() {
    local proxy_type=${1:-"backend"}
    
    case $proxy_type in
        "backend")
            echo "--build-arg HTTP_PROXY=${HTTP_PROXY:-$DEFAULT_HTTP_PROXY} \
                  --build-arg HTTPS_PROXY=${HTTPS_PROXY:-$DEFAULT_HTTPS_PROXY} \
                  --build-arg NO_PROXY=${NO_PROXY:-$DEFAULT_NO_PROXY}"
            ;;
        "frontend")
            echo "--build-arg HTTP_PROXY=${HTTP_PROXY:-$DEFAULT_HTTP_PROXY} \
                  --build-arg HTTPS_PROXY=${HTTPS_PROXY:-$DEFAULT_HTTPS_PROXY} \
                  --build-arg NO_PROXY=${NO_PROXY:-$DEFAULT_NO_PROXY}"
            ;;
        *)
            echo ""
            ;;
    esac
}

# 构建后端镜像（带代理）
build_backend_with_proxy() {
    print_info "构建后端镜像（使用代理）..."
    
    local proxy_args=$(get_proxy_config "backend")
    
    docker build \
        --file ../backend/Dockerfile.prod \
        --tag tts-flow-backend:latest \
        --no-cache \
        $proxy_args \
        ../backend
    
    print_info "后端镜像构建完成"
}

# 构建前端镜像（带代理）
build_frontend_with_proxy() {
    print_info "构建前端镜像（使用代理）..."
    
    local proxy_args=$(get_proxy_config "frontend")
    
    # 检查是否存在pnpm-lock.yaml文件
    if [ ! -f "../frontend/pnpm-lock.yaml" ]; then
        print_warning "pnpm-lock.yaml 文件不存在，将使用普通安装模式"
    fi
    
    docker build \
        --file ../frontend/Dockerfile \
        --tag tts-flow-frontend:latest \
        --no-cache \
        $proxy_args \
        ../frontend
    
    print_info "前端镜像构建完成"
}

# 构建开发环境镜像（带代理）
build_dev_with_proxy() {
    print_info "构建开发环境镜像（使用代理）..."
    
    local proxy_args=$(get_proxy_config "backend")
    
    # 后端开发镜像
    docker build \
        --file ../backend/Dockerfile \
        --tag tts-flow-backend-dev:latest \
        --no-cache \
        $proxy_args \
        ../backend
    
    proxy_args=$(get_proxy_config "frontend")
    
    # 前端开发镜像
    if [ ! -f "../frontend/pnpm-lock.yaml" ]; then
        print_warning "pnpm-lock.yaml 文件不存在，将使用普通安装模式"
    fi
    
    docker build \
        --file ../frontend/Dockerfile.dev \
        --tag tts-flow-frontend-dev:latest \
        --no-cache \
        $proxy_args \
        ../frontend
    
    print_info "开发环境镜像构建完成"
}

# 构建所有镜像（带代理）
build_all_with_proxy() {
    print_info "构建所有镜像（使用代理）..."
    
    build_backend_with_proxy
    build_frontend_with_proxy
    build_dev_with_proxy
    
    print_info "所有镜像构建完成"
}

# 显示代理配置
show_proxy_config() {
    echo ""
    print_info "当前代理配置："
    echo "----------------------------------------"
    echo "HTTP_PROXY:  ${HTTP_PROXY:-$DEFAULT_HTTP_PROXY}"
    echo "HTTPS_PROXY: ${HTTPS_PROXY:-$DEFAULT_HTTPS_PROXY}"
    echo "NO_PROXY:    ${NO_PROXY:-$DEFAULT_NO_PROXY}"
    echo "----------------------------------------"
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  backend    构建后端镜像（生产环境）"
    echo "  frontend   构建前端镜像（生产环境）"
    echo "  dev        构建开发环境镜像"
    echo "  all        构建所有镜像"
    echo "  proxy      显示当前代理配置"
    echo "  help       显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  HTTP_PROXY     - HTTP代理地址 (默认: $DEFAULT_HTTP_PROXY)"
    echo "  HTTPS_PROXY    - HTTPS代理地址 (默认: $DEFAULT_HTTPS_PROXY)"
    echo "  NO_PROXY       - 不使用代理的地址 (默认: $DEFAULT_NO_PROXY)"
    echo ""
    echo "示例:"
    echo "  $0 backend                    # 构建后端镜像"
    echo "  $0 all                        # 构建所有镜像"
    echo "  HTTP_PROXY=http://127.0.0.1:7897 $0 frontend  # 使用自定义代理"
}

# 主函数
main() {
    local action=${1:-"help"}
    
    case $action in
        "backend")
            show_proxy_config
            build_backend_with_proxy
            ;;
        "frontend")
            show_proxy_config
            build_frontend_with_proxy
            ;;
        "dev")
            show_proxy_config
            build_dev_with_proxy
            ;;
        "all")
            show_proxy_config
            build_all_with_proxy
            ;;
        "proxy")
            show_proxy_config
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