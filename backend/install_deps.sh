#!/bin/bash

echo "🔧 安装 TTS Flow Backend 依赖"
echo "================================"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  建议在虚拟环境中运行"
    echo "创建虚拟环境: python -m venv .venv"
    echo "激活虚拟环境: source .venv/bin/activate"
    echo ""
fi

# 卸载可能冲突的包
echo "🧹 清理可能冲突的包..."
pip uninstall -y motor pymongo beanie 2>/dev/null || true

# 安装指定版本的 pymongo
echo "📦 安装 pymongo 4.6.0..."
pip install pymongo==4.6.0

# 安装 motor
echo "📦 安装 motor 3.3.2..."
pip install motor==3.3.2

# 安装 beanie
echo "📦 安装 beanie 1.24.0..."
pip install beanie==1.24.0

# 安装其他依赖
echo "📦 安装其他依赖..."
pip install -r requirements.txt

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "🚀 现在可以启动服务了："
echo "   python run.py"
echo "   或者"
echo "   ./start.sh" 