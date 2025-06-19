from fastapi import APIRouter
from app.api.v1 import auth, users

api_router = APIRouter()

# 包含所有v1 API路由
api_router.include_router(auth.router)
api_router.include_router(users.router)

# API v1 Package 