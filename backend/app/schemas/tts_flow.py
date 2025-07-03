from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class TTSFlowBase(BaseModel):
    """TTS工作流基础模式"""
    name: str = Field(..., description="工作流名称")
    voiceId: Optional[str] = Field(None, description="音色ID")
    voiceName: Optional[str] = Field(None, description="音色名称")
    flow_config: Dict[str, Any] = Field(default_factory=dict, description="flow配置（JSON）")


class TTSFlowCreate(TTSFlowBase):
    """创建TTS工作流模式"""
    pass


class TTSFlowUpdate(BaseModel):
    """更新TTS工作流模式"""
    name: Optional[str] = Field(None, description="工作流名称")
    voiceId: Optional[str] = Field(None, description="音色ID")
    voiceName: Optional[str] = Field(None, description="音色名称")
    flow_config: Optional[Dict[str, Any]] = Field(None, description="flow配置（JSON）")


class TTSFlowInDB(TTSFlowBase):
    """数据库中的TTS工作流模式"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TTSFlow(TTSFlowBase):
    """API响应的TTS工作流模式"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 