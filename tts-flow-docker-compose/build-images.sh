#!/bin/bash

# TTS-Flow Docker 镜像构建脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
REGISTRY="your-registry.com"
PROJECT_NAME="tts-flow"
VERSION=${1:-"latest"}

# 代理配置（可选）
HTTP_PROXY=${HTTP_PROXY:-}
HTTPS_PROXY=${HTTPS_PROXY:-}
NO_PROXY=${NO_PROXY:-}
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

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
    echo -e "${BLUE}  TTS-Flow 镜像构建和打标脚本  ${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    print_message "Docker 环境检查通过"
}

# 构建后端镜像
build_backend_image() {
    echo "构建后端镜像..."
    docker build \
        --file ../backend/Dockerfile.prod \
        --tag "${REGISTRY}/${PROJECT_NAME}/backend:${VERSION}" \
        --tag "${REGISTRY}/${PROJECT_NAME}/backend:latest" \
        --build-arg HTTP_PROXY=${HTTP_PROXY:-} \
        --build-arg HTTPS_PROXY=${HTTPS_PROXY:-} \
        --build-arg NO_PROXY=${NO_PROXY:-} \
        ../backend
    echo "后端镜像构建完成"
}

# 构建前端镜像
build_frontend_image() {
    echo "构建前端镜像..."
    docker build \
        --file ../frontend/Dockerfile \
        --tag "${REGISTRY}/${PROJECT_NAME}/frontend:${VERSION}" \
        --tag "${REGISTRY}/${PROJECT_NAME}/frontend:latest" \
        --build-arg HTTP_PROXY=${HTTP_PROXY:-} \
        --build-arg HTTPS_PROXY=${HTTPS_PROXY:-} \
        --build-arg NO_PROXY=${NO_PROXY:-} \
        ../frontend
    echo "前端镜像构建完成"
}

# 构建开发环境镜像
build_dev_images() {
    echo "构建开发环境镜像..."
    
    # 后端开发镜像
    docker build \
        --file ../backend/Dockerfile \
        --tag "${REGISTRY}/${PROJECT_NAME}/backend-dev:${VERSION}" \
        --build-arg HTTP_PROXY=${HTTP_PROXY:-} \
        --build-arg HTTPS_PROXY=${HTTPS_PROXY:-} \
        --build-arg NO_PROXY=${NO_PROXY:-} \
        ../backend
    
    # 前端开发镜像
    docker build \
        --file ../frontend/Dockerfile.dev \
        --tag "${REGISTRY}/${PROJECT_NAME}/frontend-dev:${VERSION}" \
        --build-arg HTTP_PROXY=${HTTP_PROXY:-} \
        --build-arg HTTPS_PROXY=${HTTPS_PROXY:-} \
        --build-arg NO_PROXY=${NO_PROXY:-} \
        ../frontend
    
    echo "开发环境镜像构建完成"
}

# 推送镜像
push_images() {
    echo "推送镜像到仓库..."
    docker push "${REGISTRY}/${PROJECT_NAME}/backend:${VERSION}"
    docker push "${REGISTRY}/${PROJECT_NAME}/backend:latest"
    docker push "${REGISTRY}/${PROJECT_NAME}/frontend:${VERSION}"
    docker push "${REGISTRY}/${PROJECT_NAME}/frontend:latest"
    echo "镜像推送完成"
}

# 显示镜像信息
show_image_info() {
    echo ""
    print_message "镜像信息："
    echo "----------------------------------------"
    echo "版本: ${VERSION}"
    echo "构建时间: ${BUILD_DATE}"
    echo "Git提交: ${GIT_COMMIT}"
    echo "仓库地址: ${REGISTRY}"
    echo ""
    echo "生产环境镜像："
    echo "  后端: ${REGISTRY}/${PROJECT_NAME}/backend:${VERSION}"
    echo "  前端: ${REGISTRY}/${PROJECT_NAME}/frontend:${VERSION}"
    echo ""
    echo "开发环境镜像："
    echo "  后端: ${REGISTRY}/${PROJECT_NAME}/backend-dev:${VERSION}"
    echo "  前端: ${REGISTRY}/${PROJECT_NAME}/frontend-dev:${VERSION}"
    echo "----------------------------------------"
}

# 清理本地镜像
clean_images() {
    print_warning "这将删除所有本地构建的镜像，确定继续吗？(y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_message "清理本地镜像..."
        
        # 删除后端镜像
        docker rmi "${REGISTRY}/${PROJECT_NAME}/backend:${VERSION}" 2>/dev/null || true
        docker rmi "${REGISTRY}/${PROJECT_NAME}/backend:latest" 2>/dev/null || true
        docker rmi "${REGISTRY}/${PROJECT_NAME}/backend-dev:${VERSION}" 2>/dev/null || true
        
        # 删除前端镜像
        docker rmi "${REGISTRY}/${PROJECT_NAME}/frontend:${VERSION}" 2>/dev/null || true
        docker rmi "${REGISTRY}/${PROJECT_NAME}/frontend:latest" 2>/dev/null || true
        docker rmi "${REGISTRY}/${PROJECT_NAME}/frontend-dev:${VERSION}" 2>/dev/null || true
        
        print_message "本地镜像清理完成"
    else
        print_message "取消清理操作"
    fi
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [版本] [build|build-dev|build-all|push]"
echo ""
echo "环境变量:"
echo "  HTTP_PROXY     - HTTP代理地址 (可选)"
echo "  HTTPS_PROXY    - HTTPS代理地址 (可选)"
echo "  NO_PROXY       - 不使用代理的地址 (可选)"
echo ""
echo "示例:"
echo "  HTTP_PROXY=http://192.168.60.136:7897 $0 v1.0.0 build"
echo "  HTTPS_PROXY=http://127.0.0.1:7897 $0 latest build-all"
    echo ""
    echo "参数:"
    echo "  版本              镜像版本号 (默认: latest)"
    echo ""
    echo "选项:"
    echo "  build             构建生产环境镜像"
    echo "  build-dev         构建开发环境镜像"
    echo "  build-all         构建所有镜像"
    echo "  push              推送生产环境镜像"
    echo "  push-dev          推送开发环境镜像"
    echo "  push-all          推送所有镜像"
    echo "  clean             清理本地镜像"
    echo "  info              显示镜像信息"
    echo "  help              显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 v1.0.0 build   构建 v1.0.0 版本的生产环境镜像"
    echo "  $0 latest build-all 构建最新版本的所有镜像"
    echo "  $0 v1.0.0 push-all 推送 v1.0.0 版本的所有镜像"
}

# 主函数
main() {
    print_header
    
    local action=${2:-"build"}
    
    case $action in
        "build")
            check_docker
            build_backend_image
            build_frontend_image
            show_image_info
            ;;
        "build-dev")
            check_docker
            build_dev_images
            show_image_info
            ;;
        "build-all")
            check_docker
            build_backend_image
            build_frontend_image
            build_dev_images
            show_image_info
            ;;
        "push")
            push_images
            ;;
        "clean")
            clean_images
            ;;
        "info")
            show_image_info
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