# 自定义异常处理机制

## 概述

本项目实现了完整的自定义异常处理机制，包括异常类定义、错误码管理、统一异常处理和便捷函数。

## 异常类层次结构

```
BaseException (自定义基础异常)
├── BusinessException (业务异常)
├── ValidationException (数据验证异常)
├── AuthenticationException (认证异常)
├── AuthorizationException (授权异常)
├── NotFoundException (资源不存在异常)
└── ConflictException (资源冲突异常)
```

## 错误码定义

### 通用错误码 (1000-1999)
- `200`: 成功
- `400`: 参数错误
- `401`: 未授权访问
- `403`: 权限不足
- `404`: 资源不存在
- `409`: 资源冲突
- `422`: 数据验证失败
- `500`: 服务器内部错误

### 用户相关错误码 (1001-1099)
- `1001`: 用户不存在
- `1002`: 用户已存在
- `1003`: 密码错误
- `1004`: 账户已禁用
- `1005`: 令牌已过期
- `1006`: 令牌无效

### 业务相关错误码 (2001-2099)
- `2001`: 业务处理失败
- `2002`: 数据不存在
- `2003`: 数据已存在
- `2004`: 操作失败

### 系统相关错误码 (3001-3099)
- `3001`: 数据库错误
- `3002`: 网络错误
- `3003`: 外部服务错误

## 使用方法

### 1. 抛出业务异常

```python
from app.core.exceptions import BusinessException, ErrorCode

# 方式1: 直接抛出异常
if user_exists(username):
    raise BusinessException(
        message="用户名已存在",
        code=ErrorCode.USER_ALREADY_EXISTS
    )

# 方式2: 使用便捷函数
from app.core.exceptions import raise_business_exception

if user_not_found(user_id):
    raise_business_exception(
        code=ErrorCode.USER_NOT_FOUND,
        message="用户不存在"
    )
```

### 2. 抛出特定类型异常

```python
from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    AuthenticationException,
    ValidationException
)

# 资源不存在
if not resource_exists(resource_id):
    raise NotFoundException(
        message="资源不存在",
        code=ErrorCode.DATA_NOT_FOUND
    )

# 资源冲突
if resource_conflicts(new_data):
    raise ConflictException(
        message="资源冲突",
        code=ErrorCode.CONFLICT
    )

# 认证失败
if not verify_credentials(credentials):
    raise AuthenticationException(
        message="认证失败",
        code=ErrorCode.UNAUTHORIZED
    )

# 数据验证失败
if not validate_data(data):
    raise ValidationException(
        message="数据验证失败",
        code=ErrorCode.VALIDATION_ERROR,
        data={"field": "email", "value": data.get("email")}
    )
```

### 3. 在API路由中使用

```python
from fastapi import APIRouter
from app.core.exceptions import BusinessException, ErrorCode
from app.utils.response import success

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """获取用户信息"""
    # 业务逻辑会自动抛出异常，无需手动处理
    user = await UserService.get_user_by_id(user_id)
    return success(user.dict())
```

### 4. 异常自动处理

所有自定义异常都会被 `main.py` 中的异常处理器自动捕获并转换为统一的响应格式：

```json
{
    "code": 1001,
    "message": "用户不存在",
    "data": null
}
```

## 响应格式

### 成功响应
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        "id": "123",
        "username": "test_user"
    }
}
```

### 错误响应
```json
{
    "code": 1001,
    "message": "用户不存在",
    "data": null
}
```

## 最佳实践

### 1. 异常粒度
- 使用具体的异常类型而不是通用的 `BusinessException`
- 为不同的错误场景定义专门的异常类

### 2. 错误码管理
- 使用预定义的错误码常量
- 保持错误码的一致性和可维护性
- 为新的业务场景添加相应的错误码

### 3. 错误消息
- 提供清晰、用户友好的错误消息
- 在开发环境下可以提供更详细的错误信息
- 在生产环境下避免暴露敏感信息

### 4. 异常数据
- 使用 `data` 字段传递额外的错误信息
- 对于验证错误，可以包含具体的字段信息
- 对于业务错误，可以包含相关的上下文信息

## 扩展自定义异常

如果需要添加新的异常类型，可以继承 `BaseException`：

```python
class CustomBusinessException(BaseException):
    """自定义业务异常"""
    def __init__(
        self,
        message: str = "自定义业务错误",
        code: int = 4000,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)
```

然后在 `main.py` 中添加相应的异常处理器：

```python
@app.exception_handler(CustomBusinessException)
async def custom_business_exception_handler(request: Request, exc: CustomBusinessException):
    return fail(exc.message, code=exc.code, data=exc.data)
```

## 测试异常处理

可以使用以下方式测试异常处理：

```python
# 测试用户不存在
response = await client.get("/api/v1/users/nonexistent")
assert response.status_code == 404
assert response.json()["code"] == 1001

# 测试用户名已存在
response = await client.post("/api/v1/auth/register", json={
    "username": "existing_user",
    "email": "test@example.com",
    "password": "password123"
})
assert response.status_code == 400
assert response.json()["code"] == 1002
``` 