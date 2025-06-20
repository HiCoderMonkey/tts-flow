from fastapi import APIRouter, Request
from app.utils.response import success

router = APIRouter(prefix="/debug", tags=["调试"])


@router.get("/scope")
async def debug_scope(request: Request):
    """调试scope内容"""
    scope = request.scope
    
    # 转换scope为可序列化的格式
    debug_scope = {}
    
    # 基本信息
    debug_scope["type"] = scope.get("type")
    debug_scope["method"] = scope.get("method")
    debug_scope["path"] = scope.get("path")
    debug_scope["http_version"] = scope.get("http_version")
    debug_scope["scheme"] = scope.get("scheme")
    
    # 服务器和客户端信息
    server = scope.get("server", (None, None))
    client = scope.get("client", (None, None))
    debug_scope["server"] = f"{server[0]}:{server[1]}" if server[0] else None
    debug_scope["client"] = f"{client[0]}:{client[1]}" if client[0] else None
    
    # URL信息
    debug_scope["raw_path"] = scope.get("raw_path", b"").decode() if scope.get("raw_path") else None
    debug_scope["query_string"] = scope.get("query_string", b"").decode() if scope.get("query_string") else None
    debug_scope["root_path"] = scope.get("root_path")
    
    # 请求头
    headers = scope.get("headers", [])
    debug_scope["headers"] = {k.decode(): v.decode() for k, v in headers}
    
    # 状态信息
    debug_scope["state"] = dict(scope.get("state", {}))
    
    # 扩展信息
    debug_scope["extensions"] = scope.get("extensions", {})
    
    # 中间件添加的自定义数据
    debug_scope["user"] = scope.get("user")
    debug_scope["auth_checked"] = scope.get("auth_checked", False)
    
    return success(debug_scope)


@router.get("/request-info")
async def debug_request_info(request: Request):
    """调试请求信息"""
    return success({
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "client": f"{request.client.host}:{request.client.port}" if request.client else None,
        "user": request.scope.get("user"),
    })


@router.get("/headers")
async def debug_headers(request: Request):
    """调试请求头"""
    headers = dict(request.headers)
    
    # 隐藏敏感信息
    if "authorization" in headers:
        auth = headers["authorization"]
        if auth.startswith("Bearer "):
            token = auth[7:]  # 去掉 "Bearer "
            if len(token) > 10:
                headers["authorization"] = f"Bearer {token[:10]}..."
    
    return success(headers)


@router.get("/user-info")
async def debug_user_info(request: Request):
    """调试用户信息"""
    user = request.scope.get("user")
    
    if not user:
        return success({"message": "未找到用户信息，可能未认证或中间件未正确设置"})
    
    return success({
        "user_id": getattr(user, "id", None),
        "username": getattr(user, "username", None),
        "email": getattr(user, "email", None),
        "is_active": getattr(user, "is_active", None),
        "is_superuser": getattr(user, "is_superuser", None),
        "is_admin": getattr(user, "is_admin", None),
        "user_type": type(user).__name__,
    })


@router.get("/middleware-test")
async def test_middleware(request: Request):
    """测试中间件功能"""
    scope = request.scope
    
    # 检查中间件是否正常工作
    auth_checked = scope.get("auth_checked", False)
    user = scope.get("user")
    
    return success({
        "middleware_working": True,
        "auth_checked": auth_checked,
        "user_found": user is not None,
        "path": scope.get("path"),
        "method": scope.get("method"),
        "message": "如果看到这个响应，说明中间件正常工作"
    }) 