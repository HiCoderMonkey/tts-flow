from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TTSPlatformBase(BaseModel):
    name: str
    type: str
    status: bool = True
    config: Dict[str, Any] = {}

class TTSPlatformCreate(TTSPlatformBase):
    pass

class TTSPlatformUpdate(TTSPlatformBase):
    pass

class TTSPlatform(TTSPlatformBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 