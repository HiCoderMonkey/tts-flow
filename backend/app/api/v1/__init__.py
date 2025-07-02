from fastapi import APIRouter
from app.api.v1 import auth, users, debug, tts_flows, tts_platform, tts_voice

api_router = APIRouter()

# 包含所有v1 API路由
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(debug.router)
api_router.include_router(tts_flows.router)

# TTS资源管理路由
api_router.include_router(tts_platform.router, prefix="/tts", tags=["TTS平台管理"])
api_router.include_router(tts_voice.router, prefix="/tts", tags=["TTS音色管理"])

# API v1 Package 