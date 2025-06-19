#!/usr/bin/env python3
"""
测试 .env 文件路径
"""

from pathlib import Path

# 计算 .env 文件的绝对路径
env_path = Path(__file__).parent / ".env"

print(f"当前文件: {__file__}")
print(f".env 文件路径: {env_path}")
print(f".env 文件是否存在: {env_path.exists()}")

# 显示项目结构
print("\n项目结构:")
backend_path = Path(__file__).parent
for item in backend_path.iterdir():
    if item.is_file():
        print(f"  📄 {item.name}")
    elif item.is_dir():
        print(f"  📁 {item.name}/") 