from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from app.utils.datetime_utils import utc_now


class User(Document):
    """用户模型"""
    email: Indexed(EmailStr, unique=True)  # 邮箱，唯一索引
    username: Indexed(str, unique=True)    # 用户名，唯一索引
    hashed_password: str                   # 加密后的密码
    full_name: Optional[str] = None        # 全名
    is_active: bool = Field(default=True)  # 是否激活
    is_superuser: bool = Field(default=False)  # 是否超级用户
    created_at: datetime = Field(default_factory=utc_now)  # 创建时间
    updated_at: datetime = Field(default_factory=utc_now)  # 更新时间
    
    class Settings:
        name = "users"
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "testuser",
                "full_name": "Test User",
                "is_active": True
            }
        }
    
    def update_timestamp(self):
        """更新修改时间"""
        self.updated_at = utc_now() 