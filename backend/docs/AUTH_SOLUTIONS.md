# 统一认证和权限验证解决方案

本文档介绍了在FastAPI中统一处理登录和权限验证的几种方案，避免在每个方法中使用`Depends`。

## 方案1：中间件方式（推荐）

### 特点
- 在请求到达路由之前统一处理认证和权限
- 性能好，避免重复验证
- 配置集中，易于管理
- 支持路径级别的权限控制

### 使用方法

1. **配置权限规则**

在 `app/core/permission_config.py` 中配置权限：

```python
# 添加公开路径
permission_config.add_public_path("/api/v1/public")

# 添加路径权限
permission_config.add_path_permission("/api/v1/users/", PermissionLevel.SUPERUSER)

# 添加方法权限
permission_config.add_method_permission("/api/v1/users/me", "PUT", PermissionLevel.LOGIN)
```

2. **在路由中获取用户**

```python
from fastapi import APIRouter, Request
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/me")
async def read_users_me(request: Request):
    current_user = await get_current_active_user(request)
    return {"user": current_user}
```

### 权限级别

- `PUBLIC`: 公开访问，无需认证
- `LOGIN`: 需要登录
- `ADMIN`: 需要管理员权限
- `SUPERUSER`: 需要超级用户权限

## 方案2：装饰器方式

### 特点
- 代码简洁，易于理解
- 支持函数级别的权限控制
- 可以传递用户对象到函数参数

### 使用方法

```python
from fastapi import APIRouter, Request
from app.core.auth_decorator import require_login, require_superuser

router = APIRouter()

@router.get("/me")
@require_login
async def read_users_me(request: Request, current_user: User):
    return {"user": current_user}

@router.get("/users")
@require_superuser
async def read_users(request: Request, current_user: User):
    return {"users": []}
```

### 装饰器类型

- `@require_login`: 需要登录
- `@require_superuser`: 需要超级用户权限
- `@require_admin`: 需要管理员权限
- `@require_auth(require_active=True, require_superuser=True)`: 自定义权限

## 方案3：混合方式

可以同时使用中间件和装饰器：

- 中间件处理基础的认证和权限验证
- 装饰器处理特殊的业务逻辑权限

## 配置示例

### 权限配置文件

```python
# app/core/permission_config.py

# 公开路径
public_paths = {
    "/",
    "/health",
    "/docs",
    "/api/v1/auth/login",
    "/api/v1/auth/register"
}

# 路径权限映射
path_permissions = {
    "/api/v1/users/me": PermissionLevel.LOGIN,
    "/api/v1/users/": PermissionLevel.SUPERUSER,
    "/api/v1/admin/": PermissionLevel.ADMIN,
}

# 方法权限映射
method_permissions = {
    "/api/v1/users/me": {
        "GET": PermissionLevel.LOGIN,
        "PUT": PermissionLevel.LOGIN,
    }
}
```

### 路由示例

```python
# 使用中间件方式
@router.get("/me")
async def read_users_me(request: Request):
    current_user = await get_current_active_user(request)
    return {"user": current_user}

# 使用装饰器方式
@router.get("/me")
@require_login
async def read_users_me(request: Request, current_user: User):
    return {"user": current_user}
```

## 优势对比

| 特性 | 传统Depends | 中间件方式 | 装饰器方式 |
|------|-------------|------------|------------|
| 性能 | 每次验证 | 一次验证 | 每次验证 |
| 代码简洁性 | 需要每个路由添加 | 自动处理 | 简洁 |
| 配置集中性 | 分散 | 集中 | 分散 |
| 灵活性 | 高 | 中等 | 高 |
| 维护性 | 低 | 高 | 中等 |

## 推荐使用场景

1. **中间件方式**：适合大部分场景，特别是需要统一权限管理的项目
2. **装饰器方式**：适合需要特殊权限逻辑的场景
3. **混合方式**：适合复杂项目，基础权限用中间件，特殊逻辑用装饰器

## 注意事项

1. 中间件方式需要确保所有路由都能正确获取到用户信息
2. 装饰器方式需要注意参数顺序
3. 权限配置需要定期维护和更新
4. 建议在开发环境中启用调试模式，方便排查权限问题 