from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_current_active_user, get_current_superuser
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from app.services.user_service import UserService
from app.utils.response import success

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return success(current_user.dict())


@router.put("/me", response_model=UserSchema)
async def update_users_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """更新当前用户信息"""
    updated_user = await UserService.update_user(current_user.id, user_update)
    return success(updated_user.dict())


@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser)
):
    """获取用户列表（仅超级用户）"""
    users = await UserService.get_users(skip=skip, limit=limit)
    return success([user.dict() for user in users])


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser)
):
    """获取指定用户信息（仅超级用户）"""
    user = await UserService.get_user_by_id(user_id)
    return success(user.dict())


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_superuser)
):
    """更新指定用户信息（仅超级用户）"""
    updated_user = await UserService.update_user(user_id, user_update)
    return success(updated_user.dict())


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser)
):
    """删除用户（仅超级用户）"""
    await UserService.delete_user(user_id)
    return success({"message": "用户删除成功"}) 