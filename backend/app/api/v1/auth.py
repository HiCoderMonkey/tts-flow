from datetime import timedelta
from fastapi import APIRouter, Depends, status
from app.core.security import create_access_token
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.user import UserCreate, User, Token, UserLogin
from app.utils.response import success
from app.core.exceptions import BusinessException, ErrorCode

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate):
    """用户注册"""
    user = await UserService.create_user(user_create)
    return success(user.dict())


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    """用户登录"""
    user = await UserService.authenticate_user(user_login.username, user_login.password)
    
    if not user.is_active:
        raise BusinessException(
            message="用户未激活",
            code=ErrorCode.USER_ACCOUNT_DISABLED
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return success({"access_token": access_token, "token_type": "bearer"}) 