from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from app.core.security import verify_token
from app.core.permission_config import permission_config, PermissionLevel
from app.models.user import User
from app.schemas.user import TokenData
from app.utils.response import fail
from app.core.exceptions import (
    BusinessException,
    NotFoundException,
    ConflictException,
    ErrorCode
)

# HTTP Bearer认证
security = HTTPBearer(auto_error=False)


class AuthMiddleware:
    """认证中间件"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        path = request.url.path
        method = request.method
        
        # 检查是否为公开路径
        if permission_config.is_public_path(path):
            await self.app(scope, receive, send)
            return
        
        # 获取路径所需权限
        required_permission = permission_config.get_path_permission(path, method)
        
        # 如果是公开权限，直接通过
        if required_permission == PermissionLevel.PUBLIC:
            await self.app(scope, receive, send)
            return
        
        # 验证认证
        user = await self._authenticate_user(request)
        if not user:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"code": ErrorCode.UNAUTHORIZED, "data": {"msg": "未认证或认证失败"}}
            )
            await response(scope, receive, send)
            return
        
        # 检查权限
        if not self._check_user_permission(user, required_permission):
            response = JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"code": ErrorCode.FORBIDDEN, "data": {"msg": "权限不足"}}
            )
            await response(scope, receive, send)
            return
        
        # 将用户信息添加到请求状态中
        scope["user"] = user
        
        await self.app(scope, receive, send)
    
    async def _authenticate_user(self, request: Request) -> Optional[User]:
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
            if not user or not user.is_active:
                return None
            
            return user
            
        except Exception:
            return None
    
    def _check_user_permission(self, user: User, required_permission: PermissionLevel) -> bool:
        """检查用户权限"""
        if required_permission == PermissionLevel.LOGIN:
            return True  # 已登录用户即可
        
        if required_permission == PermissionLevel.ADMIN:
            return user.is_admin or user.is_superuser
        
        if required_permission == PermissionLevel.SUPERUSER:
            return user.is_superuser
        
        return False


def get_current_user_from_request(request: Request) -> User:
    """从请求中获取当前用户（用于依赖注入）"""
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户未认证"
        )
    return user


def get_current_active_user(request: Request) -> User:
    """获取当前活跃用户"""
    user = get_current_user_from_request(request)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    return user


def get_current_superuser(request: Request) -> User:
    """获取当前超级用户"""
    user = get_current_active_user(request)
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return user 