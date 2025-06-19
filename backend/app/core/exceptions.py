from typing import Any, Dict, Optional


class BaseException(Exception):
    """基础异常类"""
    def __init__(
        self,
        message: str = "服务器内部错误",
        code: int = 500,
        data: Optional[Any] = None
    ):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)


class BusinessException(BaseException):
    """业务异常"""
    def __init__(
        self,
        message: str = "业务处理失败",
        code: int = 400,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)


class ValidationException(BaseException):
    """数据验证异常"""
    def __init__(
        self,
        message: str = "数据验证失败",
        code: int = 422,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)


class AuthenticationException(BaseException):
    """认证异常"""
    def __init__(
        self,
        message: str = "认证失败",
        code: int = 401,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)


class AuthorizationException(BaseException):
    """授权异常"""
    def __init__(
        self,
        message: str = "权限不足",
        code: int = 403,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)


class NotFoundException(BaseException):
    """资源不存在异常"""
    def __init__(
        self,
        message: str = "资源不存在",
        code: int = 404,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)


class ConflictException(BaseException):
    """资源冲突异常"""
    def __init__(
        self,
        message: str = "资源冲突",
        code: int = 409,
        data: Optional[Any] = None
    ):
        super().__init__(message, code, data)


# 预定义的错误码
class ErrorCode:
    """错误码定义"""
    # 通用错误码
    SUCCESS = 200
    INTERNAL_ERROR = 500
    INVALID_PARAMS = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    VALIDATION_ERROR = 422
    
    # 用户相关错误码
    USER_NOT_FOUND = 1001
    USER_ALREADY_EXISTS = 1002
    USER_PASSWORD_ERROR = 1003
    USER_ACCOUNT_DISABLED = 1004
    USER_TOKEN_EXPIRED = 1005
    USER_TOKEN_INVALID = 1006
    
    # 业务相关错误码
    BUSINESS_ERROR = 2001
    DATA_NOT_FOUND = 2002
    DATA_ALREADY_EXISTS = 2003
    OPERATION_FAILED = 2004
    
    # 系统相关错误码
    DATABASE_ERROR = 3001
    NETWORK_ERROR = 3002
    EXTERNAL_SERVICE_ERROR = 3003


# 错误码对应的默认消息
ERROR_MESSAGES = {
    ErrorCode.SUCCESS: "操作成功",
    ErrorCode.INTERNAL_ERROR: "服务器内部错误",
    ErrorCode.INVALID_PARAMS: "参数错误",
    ErrorCode.UNAUTHORIZED: "未授权访问",
    ErrorCode.FORBIDDEN: "权限不足",
    ErrorCode.NOT_FOUND: "资源不存在",
    ErrorCode.CONFLICT: "资源冲突",
    ErrorCode.VALIDATION_ERROR: "数据验证失败",
    
    ErrorCode.USER_NOT_FOUND: "用户不存在",
    ErrorCode.USER_ALREADY_EXISTS: "用户已存在",
    ErrorCode.USER_PASSWORD_ERROR: "密码错误",
    ErrorCode.USER_ACCOUNT_DISABLED: "账户已禁用",
    ErrorCode.USER_TOKEN_EXPIRED: "令牌已过期",
    ErrorCode.USER_TOKEN_INVALID: "令牌无效",
    
    ErrorCode.BUSINESS_ERROR: "业务处理失败",
    ErrorCode.DATA_NOT_FOUND: "数据不存在",
    ErrorCode.DATA_ALREADY_EXISTS: "数据已存在",
    ErrorCode.OPERATION_FAILED: "操作失败",
    
    ErrorCode.DATABASE_ERROR: "数据库错误",
    ErrorCode.NETWORK_ERROR: "网络错误",
    ErrorCode.EXTERNAL_SERVICE_ERROR: "外部服务错误",
}


def get_error_message(code: int) -> str:
    """获取错误码对应的默认消息"""
    return ERROR_MESSAGES.get(code, "未知错误")


def raise_business_exception(
    code: int,
    message: Optional[str] = None,
    data: Optional[Any] = None
):
    """抛出业务异常"""
    if message is None:
        message = get_error_message(code)
    raise BusinessException(message=message, code=code, data=data) 