from typing import List, Optional
from app.models.tts_platform import TTSPlatform
from app.schemas.tts_platform import TTSPlatformCreate, TTSPlatformUpdate

class TTSPlatformCRUD:
    async def get(self, platform_id: str) -> Optional[TTSPlatform]:
        """根据ID获取平台"""
        return await TTSPlatform.get(platform_id)
    
    async def get_by_name(self, name: str) -> Optional[TTSPlatform]:
        """根据名称获取平台"""
        return await TTSPlatform.find_one(TTSPlatform.name == name)
    
    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[TTSPlatform]:
        """获取平台列表"""
        return await TTSPlatform.find_all().skip(skip).limit(limit).to_list()
    
    async def create(self, platform: TTSPlatformCreate) -> TTSPlatform:
        """创建平台"""
        db_platform = TTSPlatform(**platform.dict())
        await db_platform.insert()
        return db_platform
    
    async def update(self, platform_id: str, platform: TTSPlatformUpdate) -> Optional[TTSPlatform]:
        """更新平台"""
        db_platform = await self.get(platform_id)
        if db_platform:
            update_data = platform.dict(exclude_unset=True)
            await db_platform.update({"$set": update_data})
            db_platform.update_timestamp()
            await db_platform.save()
        return db_platform
    
    async def delete(self, platform_id: str) -> Optional[TTSPlatform]:
        """删除平台"""
        db_platform = await self.get(platform_id)
        if db_platform:
            await db_platform.delete()
        return db_platform

    async def count(self) -> int:
        return await TTSPlatform.count()

# 创建CRUD实例
tts_platform_crud = TTSPlatformCRUD() 