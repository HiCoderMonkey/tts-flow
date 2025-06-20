from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from app.core.auth_middleware import get_current_user_from_request, get_current_active_user, get_current_superuser
from app.models.user import User

# 新的依赖函数，从中间件获取用户信息
async def get_current_user(request: Request) -> User:
    """获取当前用户（从中间件）"""
    return get_current_user_from_request(request)


async def get_current_active_user_dep(request: Request) -> User:
    """获取当前活跃用户（从中间件）"""
    return get_current_active_user(request)


async def get_current_superuser_dep(request: Request) -> User:
    """获取当前超级用户（从中间件）"""
    return get_current_superuser(request)


# 为了向后兼容，保留原有的函数名
get_current_active_user = get_current_active_user_dep
get_current_superuser = get_current_superuser_dep 