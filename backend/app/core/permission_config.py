from typing import Dict, List, Set
from enum import Enum


class PermissionLevel(Enum):
    """权限级别枚举"""
    PUBLIC = "public"           # 公开访问
    LOGIN = "login"             # 需要登录
    ADMIN = "admin"             # 需要管理员权限
    SUPERUSER = "superuser"     # 需要超级用户权限


class PermissionConfig:
    """权限配置类"""
    
    def __init__(self):
        # 公开路径（不需要认证）
        self.public_paths: Set[str] = {
            "/docs",
            "/static",
            "/favicon.ico"
            "/.well-known",
            "/health",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh",
            "/api/v1/auth/forgot-password",
            "/api/v1/auth/reset-password"
        }
        
        # 路径权限映射
        self.path_permissions: Dict[str, PermissionLevel] = {
            # 用户相关
            "/api/v1/users/me": PermissionLevel.LOGIN,
            "/api/v1/users/": PermissionLevel.SUPERUSER,
            "/api/v1/users/{user_id}": PermissionLevel.SUPERUSER,

            # tts工作流相关
            "/api/v1/tts-flows": PermissionLevel.LOGIN,
            
            # 管理员相关
            "/api/v1/admin/": PermissionLevel.ADMIN,
            "/api/v1/admin/users": PermissionLevel.SUPERUSER,
            "/api/v1/admin/system": PermissionLevel.SUPERUSER,
            
            # 业务相关
            "/api/v1/tts/": PermissionLevel.LOGIN,
            "/api/v1/tts/history": PermissionLevel.LOGIN,
            "/api/v1/tts/admin": PermissionLevel.ADMIN,
            
            # 文件相关
            "/api/v1/files/upload": PermissionLevel.LOGIN,
            "/api/v1/files/download": PermissionLevel.LOGIN,
            "/api/v1/files/admin": PermissionLevel.ADMIN,
        }
        
        # 方法权限映射（可以覆盖路径权限）
        self.method_permissions: Dict[str, Dict[str, PermissionLevel]] = {
            "/api/v1/users/me": {
                "GET": PermissionLevel.LOGIN,
                "PUT": PermissionLevel.LOGIN,
            },
            "/api/v1/users/": {
                "GET": PermissionLevel.SUPERUSER,
                "POST": PermissionLevel.SUPERUSER,
            },
            "/api/v1/users/{user_id}": {
                "GET": PermissionLevel.SUPERUSER,
                "PUT": PermissionLevel.SUPERUSER,
                "DELETE": PermissionLevel.SUPERUSER,
            }
        }
    
    def is_public_path(self, path: str) -> bool:
        """检查是否为公开路径"""
        # 精确匹配
        if path in self.public_paths:
            return True
        
        # 只对非根路径做前缀匹配
        for public_path in self.public_paths:
            if public_path != "/" and path.startswith(public_path):
                return True
        
        return False
    
    def get_path_permission(self, path: str, method: str = "GET") -> PermissionLevel:
        """获取路径权限级别"""
        # 首先检查方法级别的权限
        if path in self.method_permissions:
            if method in self.method_permissions[path]:
                return self.method_permissions[path][method]
        
        # 然后检查路径级别的权限
        for pattern, permission in self.path_permissions.items():
            if self._match_path_pattern(path, pattern):
                return permission
        
        # 默认需要登录
        return PermissionLevel.LOGIN
    
    def _match_path_pattern(self, path: str, pattern: str) -> bool:
        """匹配路径模式"""
        # 简单的路径匹配，支持 {param} 参数
        if pattern == path:
            return True
        
        # 处理参数化路径
        if "{user_id}" in pattern:
            pattern_parts = pattern.split("/")
            path_parts = path.split("/")
            
            if len(pattern_parts) != len(path_parts):
                return False
            
            for i, pattern_part in enumerate(pattern_parts):
                if pattern_part.startswith("{") and pattern_part.endswith("}"):
                    continue  # 参数部分，跳过
                if pattern_part != path_parts[i]:
                    return False
            
            return True
        
        # 前缀匹配
        return path.startswith(pattern)
    
    def add_public_path(self, path: str):
        """添加公开路径"""
        self.public_paths.add(path)
    
    def add_path_permission(self, path: str, permission: PermissionLevel):
        """添加路径权限"""
        self.path_permissions[path] = permission
    
    def add_method_permission(self, path: str, method: str, permission: PermissionLevel):
        """添加方法权限"""
        if path not in self.method_permissions:
            self.method_permissions[path] = {}
        self.method_permissions[path][method] = permission


# 全局权限配置实例
permission_config = PermissionConfig() 