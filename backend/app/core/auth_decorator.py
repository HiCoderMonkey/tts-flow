from functools import wraps
from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from app.models.user import User
from app.core.security import verify_token
from app.utils.response import fail


def require_auth(require_active: bool = True, require_superuser: bool = False, require_admin: bool = False):
    """
    认证装饰器
    
    Args:
        require_active: 是否需要活跃用户
        require_superuser: 是否需要超级用户权限
        require_admin: 是否需要管理员权限
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从参数中获取request
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="无法获取请求对象"
                )
            
            # 验证用户
            user = await _authenticate_user(request)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="未认证或认证失败"
                )
            
            # 检查用户状态
            if require_active and not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户未激活"
                )
            
            # 检查权限
            if require_superuser and not user.is_superuser:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="需要超级用户权限"
                )
            
            if require_admin and not user.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="需要管理员权限"
                )
            
            # 将用户添加到kwargs中
            kwargs['current_user'] = user
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


async def _authenticate_user(request: Request) -> Optional[User]:
    """认证用户"""
    try:
        # 获取Authorization头
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            return None
        
        username = payload.get("sub")
        if not username:
            return None
        
        # 从数据库获取用户
        user = await User.find_one({"username": username})
        if not user:
            return None
        
        return user
        
    except Exception:
        return None


# 便捷装饰器
def require_login(func: Callable):
    """需要登录装饰器"""
    return require_auth(require_active=True)(func)


def require_superuser(func: Callable):
    """需要超级用户装饰器"""
    return require_auth(require_active=True, require_superuser=True)(func)


def require_admin(func: Callable):
    """需要管理员装饰器"""
    return require_auth(require_active=True, require_admin=True)(func) 