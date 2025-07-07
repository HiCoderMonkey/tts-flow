#!/bin/bash

# TTS-Flow 生成Lock文件脚本

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

# 检查Node.js和pnpm
check_environment() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js 未安装"
        exit 1
    fi
    
    if ! command -v pnpm &> /dev/null; then
        print_warning "pnpm 未安装，正在安装..."
        npm install -g pnpm
    fi
    
    print_info "环境检查通过"
}

# 生成前端lock文件
generate_frontend_lockfile() {
    print_info "生成前端 lock 文件..."
    
    cd ../frontend
    
    # 备份现有的lock文件
    if [ -f "pnpm-lock.yaml" ]; then
        print_info "备份现有的 pnpm-lock.yaml 文件"
        cp pnpm-lock.yaml pnpm-lock.yaml.backup
    fi
    
    # 清理node_modules
    if [ -d "node_modules" ]; then
        print_info "清理现有的 node_modules"
        rm -rf node_modules
    fi
    
    # 安装依赖并生成lock文件
    print_info "安装依赖并生成 lock 文件..."
    pnpm install
    
    if [ -f "pnpm-lock.yaml" ]; then
        print_info "pnpm-lock.yaml 文件生成成功"
    else
        print_error "pnpm-lock.yaml 文件生成失败"
        exit 1
    fi
    
    cd ../tts-flow-docker-compose
}

# 生成后端lock文件（如果有requirements.txt.lock）
generate_backend_lockfile() {
    print_info "检查后端依赖..."
    
    cd ../backend
    
    if [ -f "requirements.txt" ]; then
        print_info "发现 requirements.txt 文件"
        
        # 可以在这里添加Python依赖锁定逻辑
        # 例如使用 pip-tools 生成 requirements.txt.lock
        print_info "后端依赖检查完成"
    fi
    
    cd ../tts-flow-docker-compose
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  frontend    生成前端 pnpm-lock.yaml 文件"
    echo "  backend     检查后端依赖（可选）"
    echo "  all         生成所有lock文件"
    echo "  help        显示此帮助信息"
    echo ""
    echo "说明:"
    echo "  此脚本用于生成依赖锁定文件，确保Docker构建的一致性"
    echo "  建议在修改依赖后运行此脚本"
}

# 主函数
main() {
    local action=${1:-"help"}
    
    case $action in
        "frontend")
            check_environment
            generate_frontend_lockfile
            ;;
        "backend")
            check_environment
            generate_backend_lockfile
            ;;
        "all")
            check_environment
            generate_frontend_lockfile
            generate_backend_lockfile
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