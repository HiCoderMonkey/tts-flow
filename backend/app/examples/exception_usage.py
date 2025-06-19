"""
自定义异常使用示例
"""

from app.core.exceptions import (
    BusinessException,
    NotFoundException,
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ErrorCode,
    raise_business_exception
)


def example_business_logic():
    """业务逻辑示例"""
    
    # 示例1: 用户不存在
    user_id = "123"
    if not user_exists(user_id):
        raise NotFoundException(
            message=f"用户 {user_id} 不存在",
            code=ErrorCode.USER_NOT_FOUND
        )
    
    # 示例2: 用户名已存在
    username = "test_user"
    if username_exists(username):
        raise ConflictException(
            message=f"用户名 {username} 已存在",
            code=ErrorCode.USER_ALREADY_EXISTS
        )
    
    # 示例3: 密码错误
    password = "wrong_password"
    if not verify_password(password):
        raise AuthenticationException(
            message="密码错误",
            code=ErrorCode.USER_PASSWORD_ERROR
        )
    
    # 示例4: 权限不足
    if not has_permission("admin"):
        raise AuthorizationException(
            message="需要管理员权限",
            code=ErrorCode.FORBIDDEN
        )
    
    # 示例5: 数据验证失败
    email = "invalid_email"
    if not is_valid_email(email):
        raise ValidationException(
            message="邮箱格式不正确",
            code=ErrorCode.VALIDATION_ERROR,
            data={"field": "email", "value": email}
        )
    
    # 示例6: 使用便捷函数
    if some_business_rule_failed():
        raise_business_exception(
            code=ErrorCode.BUSINESS_ERROR,
            message="业务规则验证失败",
            data={"rule": "some_rule"}
        )


def user_exists(user_id: str) -> bool:
    """检查用户是否存在"""
    return False  # 模拟用户不存在


def username_exists(username: str) -> bool:
    """检查用户名是否存在"""
    return True  # 模拟用户名已存在


def verify_password(password: str) -> bool:
    """验证密码"""
    return False  # 模拟密码错误


def has_permission(permission: str) -> bool:
    """检查权限"""
    return False  # 模拟权限不足


def is_valid_email(email: str) -> bool:
    """验证邮箱格式"""
    return False  # 模拟邮箱格式错误


def some_business_rule_failed() -> bool:
    """检查业务规则"""
    return True  # 模拟业务规则失败


# API路由中使用示例
async def api_example():
    """API路由中的异常处理示例"""
    
    try:
        # 执行业务逻辑
        result = await perform_business_operation()
        return {"success": True, "data": result}
        
    except NotFoundException as e:
        # 404错误 - 资源不存在
        return {"success": False, "code": e.code, "message": e.message}
        
    except ConflictException as e:
        # 409错误 - 资源冲突
        return {"success": False, "code": e.code, "message": e.message}
        
    except AuthenticationException as e:
        # 401错误 - 认证失败
        return {"success": False, "code": e.code, "message": e.message}
        
    except AuthorizationException as e:
        # 403错误 - 权限不足
        return {"success": False, "code": e.code, "message": e.message}
        
    except ValidationException as e:
        # 422错误 - 数据验证失败
        return {"success": False, "code": e.code, "message": e.message, "data": e.data}
        
    except BusinessException as e:
        # 400错误 - 业务错误
        return {"success": False, "code": e.code, "message": e.message, "data": e.data}
        
    except Exception as e:
        # 500错误 - 服务器内部错误
        return {"success": False, "code": 500, "message": "服务器内部错误"}


async def perform_business_operation():
    """执行业务操作"""
    # 这里会抛出各种异常
    example_business_logic()
    return {"result": "success"} 