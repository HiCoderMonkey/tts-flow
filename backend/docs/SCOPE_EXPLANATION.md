# FastAPI/ASGI Scope 详细解释

## 什么是 Scope？

`scope` 是ASGI（Asynchronous Server Gateway Interface）规范中的核心概念，它是一个字典，包含了HTTP请求的所有信息。在FastAPI中，每个请求都会创建一个scope字典，并在整个请求生命周期中传递。

## Scope 的生命周期

```
客户端请求 → ASGI服务器 → FastAPI应用 → 中间件 → 路由处理函数 → 响应
     ↓           ↓           ↓         ↓        ↓
  创建scope → 传递scope → 修改scope → 读取scope → 返回响应
```

## Scope 字典的完整结构

### 1. 基本信息
```python
{
    "type": "http",                    # 请求类型
    "asgi": {                         # ASGI版本信息
        "version": "3.0",
        "spec_version": "2.0"
    }
}
```

### 2. HTTP请求信息
```python
{
    "http_version": "1.1",             # HTTP版本
    "method": "GET",                   # HTTP方法
    "scheme": "https",                 # 协议（http/https）
    "server": ("example.com", 443),    # 服务器地址和端口
    "client": ("192.168.1.1", 12345),  # 客户端地址和端口
}
```

### 3. URL信息
```python
{
    "path": "/api/v1/users/me",        # 请求路径
    "raw_path": b"/api/v1/users/me",   # 原始路径（字节）
    "query_string": b"page=1&limit=10", # 查询字符串
    "root_path": "",                   # 根路径
}
```

### 4. 请求头
```python
{
    "headers": [
        (b"host", b"example.com"),
        (b"user-agent", b"Mozilla/5.0..."),
        (b"authorization", b"Bearer token123"),
        (b"content-type", b"application/json"),
        (b"accept", b"application/json"),
    ]
}
```

### 5. 状态信息
```python
{
    "state": {},                       # 应用状态（可修改）
    "extensions": {},                  # 扩展信息
    "app": None,                       # 应用实例
}
```

## 在中间件中使用 Scope

### 基本用法
```python
class AuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # 1. 检查请求类型
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # 2. 获取请求信息
        path = scope["path"]
        method = scope["method"]
        
        # 3. 获取请求头
        headers = dict(scope["headers"])
        auth_header = headers.get(b"authorization", b"").decode()
        
        # 4. 在scope中添加自定义数据
        scope["user"] = {"id": 123, "username": "test"}
        scope["auth_checked"] = True
        
        # 5. 继续处理请求
        await self.app(scope, receive, send)
```

### 权限验证示例
```python
async def __call__(self, scope, receive, send):
    if scope["type"] != "http":
        await self.app(scope, receive, send)
        return
    
    request = Request(scope, receive)
    path = request.url.path
    method = request.method
    
    # 检查权限
    required_permission = permission_config.get_path_permission(path, method)
    
    # 验证用户
    user = await self._authenticate_user(request)
    if not user:
        # 返回401错误
        response = JSONResponse(
            status_code=401,
            content={"error": "未认证"}
        )
        await response(scope, receive, send)
        return
    
    # 将用户信息添加到scope
    scope["user"] = user
    
    await self.app(scope, receive, send)
```

## 在路由中访问 Scope

### 通过 Request 对象
```python
from fastapi import Request

@router.get("/me")
async def read_users_me(request: Request):
    # 获取scope
    scope = request.scope
    
    # 获取路径
    path = scope["path"]
    
    # 获取用户信息（由中间件添加）
    user = scope.get("user")
    
    # 获取请求头
    headers = dict(scope["headers"])
    user_agent = headers.get(b"user-agent", b"").decode()
    
    return {
        "user": user,
        "path": path,
        "user_agent": user_agent
    }
```

### 直接访问 scope
```python
@router.get("/debug")
async def debug_scope(request: Request):
    scope = request.scope
    
    return {
        "type": scope["type"],
        "method": scope["method"],
        "path": scope["path"],
        "headers": {k.decode(): v.decode() for k, v in scope["headers"]},
        "client": scope["client"],
        "server": scope["server"],
        "user": scope.get("user"),  # 中间件添加的数据
    }
```

## Scope 的重要特性

### 1. 可修改性
- 中间件可以修改scope的内容
- 添加自定义数据：`scope["user"] = user`
- 添加状态信息：`scope["auth_checked"] = True`

### 2. 传递性
- scope在整个请求生命周期中传递
- 中间件 → 路由 → 依赖注入 → 响应

### 3. 请求级别
- 每个请求都有独立的scope
- 不同请求之间不会相互影响

### 4. 类型安全
- scope是字典类型
- 可以存储任何类型的数据

## 实际应用场景

### 1. 认证中间件
```python
# 在scope中存储用户信息
scope["user"] = authenticated_user
scope["auth_checked"] = True
```

### 2. 日志中间件
```python
# 在scope中存储请求ID
scope["request_id"] = generate_request_id()
```

### 3. 性能监控
```python
# 在scope中存储开始时间
scope["start_time"] = time.time()
```

### 4. 权限验证
```python
# 在scope中存储权限信息
scope["permissions"] = user_permissions
```

## 注意事项

### 1. 数据类型
- 请求头是字节类型：`b"authorization"`
- 需要解码：`auth_header.decode()`

### 2. 键名约定
- 使用小写字母和下划线
- 避免与ASGI标准键冲突

### 3. 性能考虑
- scope在整个请求中传递，避免存储大量数据
- 及时清理不需要的数据

### 4. 错误处理
- 检查键是否存在：`scope.get("user")`
- 提供默认值：`scope.get("user", None)`

## 调试技巧

### 1. 打印完整scope
```python
import json

@router.get("/debug-scope")
async def debug_full_scope(request: Request):
    scope = request.scope
    
    # 转换字节为字符串
    debug_scope = {}
    for key, value in scope.items():
        if isinstance(value, bytes):
            debug_scope[key] = value.decode()
        elif isinstance(value, list) and key == "headers":
            debug_scope[key] = {k.decode(): v.decode() for k, v in value}
        else:
            debug_scope[key] = value
    
    return debug_scope
```

### 2. 中间件调试
```python
async def __call__(self, scope, receive, send):
    print(f"请求路径: {scope['path']}")
    print(f"请求方法: {scope['method']}")
    print(f"请求头: {dict(scope['headers'])}")
    
    await self.app(scope, receive, send)
```

## 总结

Scope是ASGI/FastAPI中传递请求信息的核心机制：

1. **包含所有请求信息**：路径、方法、头部、客户端信息等
2. **可修改和扩展**：中间件可以添加自定义数据
3. **请求级别隔离**：每个请求有独立的scope
4. **全生命周期传递**：从中间件到路由处理函数

理解scope对于开发中间件、自定义认证、权限验证等功能非常重要。 