from datetime import datetime
from typing import Optional, Dict, Any
from beanie import Document, Indexed
from pydantic import Field
from app.utils.datetime_utils import utc_now


class TTSPlatform(Document):
    """TTS平台模型"""
    name: Indexed(str, unique=True)  # 平台名称，唯一索引
    type: str = Field(..., description="平台类型")
    status: bool = Field(default=True, description="状态")
    config: Dict[str, Any] = Field(default_factory=dict, description="平台配置JSON")
    created_at: datetime = Field(default_factory=utc_now, description="创建时间")
    updated_at: datetime = Field(default_factory=utc_now, description="更新时间")
    
    class Settings:
        name = "tts_platforms"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "火山引擎",
                "type": "volcano",
                "status": True,
                "config": {
                    "appid": "your_app_id",
                    "access_token": "your_access_token"
                }
            }
        }
    
    def update_timestamp(self):
        """更新修改时间"""
        self.updated_at = utc_now() 