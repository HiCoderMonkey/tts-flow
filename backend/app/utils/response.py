from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse

# code到http状态码的映射
CODE_HTTP_MAP = {
    200: status.HTTP_200_OK,
    400: status.HTTP_400_BAD_REQUEST,
    401: status.HTTP_401_UNAUTHORIZED,
    403: status.HTTP_403_FORBIDDEN,
    404: status.HTTP_404_NOT_FOUND,
    409: status.HTTP_409_CONFLICT,
    422: status.HTTP_422_UNPROCESSABLE_ENTITY,
    500: status.HTTP_500_INTERNAL_SERVER_ERROR,
}

def success(data: Any = None, code: int = 200):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"code": code, "data": data}
    )

def fail(msg: str = "error", code: int = 1, status_code: int = None, data: Any = None):
    # 优先使用传入的status_code，否则根据code自动映射
    http_code = CODE_HTTP_MAP.get(code, status.HTTP_400_BAD_REQUEST)
    return JSONResponse(
        status_code=http_code,
        content={"code": code, "data": {"msg": msg} if data is None else data}
    ) 