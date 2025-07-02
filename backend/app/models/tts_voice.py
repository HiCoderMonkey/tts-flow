from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field
from app.utils.datetime_utils import utc_now


class TTSVoice(Document):
    """TTS音色模型"""
    name: Indexed(str, unique=True)  # 音色名称，唯一索引
    platform_id: str = Field(..., description="关联平台ID")
    role_id: str = Field(..., description="角色ID")
    status: bool = Field(default=True, description="状态")
    extension_json: str = Field(default="{}", description="扩展属性JSON")
    created_at: datetime = Field(default_factory=utc_now, description="创建时间")
    updated_at: datetime = Field(default_factory=utc_now, description="更新时间")
    
    class Settings:
        name = "tts_voices"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "小冰音色",
                "platform_id": "507f1f77bcf86cd799439011",
                "role_id": "xiaoice_001",
                "status": True,
                "extension_json": "{\"gender\": \"female\", \"language\": \"zh-CN\"}"
            }
        }
    
    def update_timestamp(self):
        """更新修改时间"""
        self.updated_at = utc_now() 