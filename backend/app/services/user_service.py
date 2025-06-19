from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import (
    BusinessException,
    NotFoundException,
    ConflictException,
    ErrorCode
)


class UserService:
    """用户服务"""
    
    @staticmethod
    async def create_user(user_create: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        existing_user = await User.find_one({"username": user_create.username})
        if existing_user:
            raise BusinessException(
                message="用户名已存在",
                code=ErrorCode.USER_ALREADY_EXISTS
            )
        
        # 检查邮箱是否已存在
        existing_email = await User.find_one({"email": user_create.email})
        if existing_email:
            raise BusinessException(
                message="邮箱已存在",
                code=ErrorCode.USER_ALREADY_EXISTS
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=user_create.is_active
        )
        
        await user.insert()
        return user
    
    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[User]:
        """验证用户"""
        user = await User.find_one({"username": username})
        if not user:
            raise BusinessException(
                message="用户不存在",
                code=ErrorCode.USER_NOT_FOUND
            )
        
        if not verify_password(password, user.hashed_password):
            raise BusinessException(
                message="密码错误",
                code=ErrorCode.USER_PASSWORD_ERROR
            )
        
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        user = await User.get(user_id)
        if not user:
            raise NotFoundException(
                message="用户不存在",
                code=ErrorCode.USER_NOT_FOUND
            )
        return user
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        user = await User.find_one({"username": username})
        if not user:
            raise NotFoundException(
                message="用户不存在",
                code=ErrorCode.USER_NOT_FOUND
            )
        return user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        user = await User.find_one({"email": email})
        if not user:
            raise NotFoundException(
                message="用户不存在",
                code=ErrorCode.USER_NOT_FOUND
            )
        return user
    
    @staticmethod
    async def update_user(user_id: str, user_update: UserUpdate) -> Optional[User]:
        """更新用户"""
        user = await User.get(user_id)
        if not user:
            raise NotFoundException(
                message="用户不存在",
                code=ErrorCode.USER_NOT_FOUND
            )
        
        update_data = user_update.dict(exclude_unset=True)
        
        # 如果更新密码，需要加密
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # 检查用户名唯一性
        if "username" in update_data:
            existing_user = await User.find_one({"username": update_data["username"]})
            if existing_user and existing_user.id != user_id:
                raise ConflictException(
                    message="用户名已存在",
                    code=ErrorCode.USER_ALREADY_EXISTS
                )
        
        # 检查邮箱唯一性
        if "email" in update_data:
            existing_user = await User.find_one({"email": update_data["email"]})
            if existing_user and existing_user.id != user_id:
                raise ConflictException(
                    message="邮箱已存在",
                    code=ErrorCode.USER_ALREADY_EXISTS
                )
        
        # 更新用户
        await user.update({"$set": update_data})
        user.update_timestamp()
        await user.save()
        
        return user
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """删除用户"""
        user = await User.get(user_id)
        if not user:
            raise NotFoundException(
                message="用户不存在",
                code=ErrorCode.USER_NOT_FOUND
            )
        
        await user.delete()
        return True
    
    @staticmethod
    async def get_users(skip: int = 0, limit: int = 100):
        """获取用户列表"""
        return await User.find_all().skip(skip).limit(limit).to_list() 