from fastapi import APIRouter
from app.api.v1 import auth, users, debug, tts_flows

api_router = APIRouter()

# 包含所有v1 API路由
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(debug.router)
api_router.include_router(tts_flows.router)

# API v1 Package 