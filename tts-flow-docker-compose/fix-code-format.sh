#!/bin/bash

# TTS-Flow 代码格式修复脚本

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

# 检查环境
check_environment() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js 未安装"
        exit 1
    fi
    
    print_info "环境检查通过"
}

# 修复前端代码格式
fix_frontend_format() {
    print_info "修复前端代码格式..."
    
    cd ../frontend
    
    # 检查package.json是否存在
    if [ ! -f "package.json" ]; then
        print_error "package.json 文件不存在"
        exit 1
    fi
    
    # 安装依赖（如果需要）
    if [ ! -d "node_modules" ]; then
        print_info "安装依赖..."
        if command -v pnpm &> /dev/null; then
            pnpm install
        else
            npm install
        fi
    fi
    
    # 修复代码格式
    print_info "运行 Prettier 格式化..."
    if command -v pnpm &> /dev/null; then
        pnpm lint:format || print_warning "Prettier 格式化失败，继续执行..."
    else
        npm run lint:format || print_warning "Prettier 格式化失败，继续执行..."
    fi
    
    # 修复 ESLint 问题
    print_info "运行 ESLint 自动修复..."
    if command -v pnpm &> /dev/null; then
        pnpm lint:eslint --fix || print_warning "ESLint 修复失败，继续执行..."
    else
        npm run lint:eslint --fix || print_warning "ESLint 修复失败，继续执行..."
    fi
    
    # 检查修复结果
    print_info "检查修复结果..."
    if command -v pnpm &> /dev/null; then
        pnpm lint:eslint || print_warning "仍有 ESLint 错误，但已尝试修复"
    else
        npm run lint:eslint || print_warning "仍有 ESLint 错误，但已尝试修复"
    fi
    
    print_info "前端代码格式修复完成"
    cd ../tts-flow-docker-compose
}

# 修复后端代码格式（如果有Python代码）
fix_backend_format() {
    print_info "检查后端代码格式..."
    
    cd ../backend
    
    # 检查是否有Python代码
    if [ -f "requirements.txt" ]; then
        print_info "发现Python项目，检查代码格式..."
        
        # 检查是否安装了black
        if command -v black &> /dev/null; then
            print_info "使用 black 格式化Python代码..."
            find . -name "*.py" -exec black {} \; || print_warning "black 格式化失败"
        else
            print_warning "black 未安装，跳过Python代码格式化"
        fi
        
        # 检查是否安装了flake8
        if command -v flake8 &> /dev/null; then
            print_info "检查Python代码风格..."
            flake8 . || print_warning "flake8 检查发现问题"
        else
            print_warning "flake8 未安装，跳过Python代码风格检查"
        fi
    fi
    
    cd ../tts-flow-docker-compose
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  frontend    修复前端代码格式"
    echo "  backend     修复后端代码格式（可选）"
    echo "  all         修复所有代码格式"
    echo "  help        显示此帮助信息"
    echo ""
    echo "说明:"
    echo "  此脚本用于修复代码格式问题，解决构建时的ESLint和Prettier错误"
    echo "  建议在构建前运行此脚本"
}

# 主函数
main() {
    local action=${1:-"help"}
    
    case $action in
        "frontend")
            check_environment
            fix_frontend_format
            ;;
        "backend")
            check_environment
            fix_backend_format
            ;;
        "all")
            check_environment
            fix_frontend_format
            fix_backend_format
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