from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz

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

def to_shanghai(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

def convert_datetime_to_shanghai(obj):
    if isinstance(obj, dict):
        return {k: convert_datetime_to_shanghai(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_shanghai(i) for i in obj]
    elif isinstance(obj, datetime):
        return to_shanghai(obj)
    else:
        return obj

def success(data: Any = None, code: int = 200):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"code": code, "data": jsonable_encoder(convert_datetime_to_shanghai(data))}
    )

def fail(msg: str = "error", code: int = 1, status_code: int = None, data: Any = None):
    # 优先使用传入的status_code，否则根据code自动映射
    http_code = CODE_HTTP_MAP.get(code, status.HTTP_400_BAD_REQUEST)
    return JSONResponse(
        status_code=http_code,
        content={"code": code, "data": jsonable_encoder(convert_datetime_to_shanghai({"msg": msg} if data is None else data))}
    ) 