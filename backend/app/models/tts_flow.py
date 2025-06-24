from datetime import datetime
from typing import Dict, Any
from beanie import Document, Indexed
from pydantic import Field
from app.utils.datetime_utils import utc_now


class TTSFlow(Document):
    """TTS工作流模型"""
    name: Indexed(str)  # 工作流名称
    flow_config: Dict[str, Any] = Field(default_factory=dict)  # flow配置（JSON）
    created_at: datetime = Field(default_factory=utc_now)  # 创建时间
    updated_at: datetime = Field(default_factory=utc_now)  # 更新时间
    
    class Settings:
        name = "tts_flows"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "默认TTS工作流",
                "flow_config": {
                    "steps": [
                        {
                            "id": "text_input",
                            "type": "input",
                            "config": {
                                "placeholder": "请输入要转换的文本"
                            }
                        },
                        {
                            "id": "tts_engine",
                            "type": "tts",
                            "config": {
                                "voice": "zh-CN-XiaoxiaoNeural",
                                "speed": 1.0
                            }
                        }
                    ]
                }
            }
        }
    
    def update_timestamp(self):
        """更新修改时间"""
        self.updated_at = utc_now() 