from fastapi import APIRouter
from app.api.v1 import auth, users, debug, tts_flows, tts_platform, tts_voice, tts_synthesize, role
from .tts_flows import router as tts_flows_router
from .tts_voice import router as tts_voice_router
from .tts_platform import router as tts_platform_router
from .tts_synthesize import router as tts_synthesize_router
from .role import router as role_router 

api_router = APIRouter()

# 包含所有v1 API路由
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(debug.router)
api_router.include_router(tts_flows.router)
api_router.include_router(tts_synthesize.router)

# 角色资源
api_router.include_router(role_router)

# TTS资源管理路由
api_router.include_router(tts_platform.router, prefix="/tts", tags=["TTS平台管理"])
api_router.include_router(tts_voice.router, prefix="/tts", tags=["TTS音色管理"])

# API v1 Package 

routers = [
    tts_flows_router,
    tts_voice_router,
    tts_platform_router,
    tts_synthesize_router,
    role_router
] 