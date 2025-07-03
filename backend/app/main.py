from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.auth_middleware import AuthMiddleware
from app.api.v1 import api_router
from app.utils.response import fail, success
from app.core.exceptions import (
    BaseException,
    BusinessException,
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    NotFoundException,
    ConflictException
)
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源
    await close_db()


# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="TTS Flow 后端API服务",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
    docs_url=None,  # 禁用默认的 /docs
    redoc_url=None  # 禁用默认的 /redoc
)

# 添加认证中间件
app.add_middleware(AuthMiddleware)

# 自定义异常处理
@app.exception_handler(BaseException)
async def custom_exception_handler(request: Request, exc: BaseException):
    """自定义异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """业务异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    """验证异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

@app.exception_handler(AuthenticationException)
async def authentication_exception_handler(request: Request, exc: AuthenticationException):
    """认证异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

@app.exception_handler(AuthorizationException)
async def authorization_exception_handler(request: Request, exc: AuthorizationException):
    """授权异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """资源不存在异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    """资源冲突异常处理器"""
    return fail(exc.message, code=exc.code, data=exc.data, status_code=exc.code)

# 全局异常处理
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return fail(str(exc), code=400, status_code=400)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return fail(exc.detail, code=exc.status_code, status_code=exc.status_code)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    msg = f"服务器内部错误: {str(exc)}" if settings.debug else "服务器内部错误"
    return fail(msg, code=500, status_code=500)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
from app.core.constants import AppConstants
app.mount("/static", StaticFiles(directory=AppConstants.STATIC_DIR), name="static")

# 包含API路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return success({
        "message": "欢迎使用 TTS Flow 后端API",
        "version": "1.0.0",
        "docs": "/docs"
    })


@app.get("/health")
async def health_check():
    """健康检查"""
    return success({"status": "healthy"})


@app.get("/docs")
async def custom_docs():
    """自定义API文档页面"""
    from fastapi.responses import FileResponse
    docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "docs.html")
    return FileResponse(docs_path) 