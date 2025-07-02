from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TTSVoiceBase(BaseModel):
    name: str
    platformId: str
    roleId: str
    status: bool = True
    extensionJson: str = "{}"

class TTSVoiceCreate(TTSVoiceBase):
    pass

class TTSVoiceUpdate(TTSVoiceBase):
    pass

class TTSVoice(TTSVoiceBase):
    id: str
    platformName: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 