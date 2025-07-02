from typing import List, Optional
from app.models.tts_voice import TTSVoice
from app.models.tts_platform import TTSPlatform
from app.schemas.tts_voice import TTSVoiceCreate, TTSVoiceUpdate

class TTSVoiceCRUD:
    async def get(self, voice_id: str) -> Optional[TTSVoice]:
        """根据ID获取音色"""
        return await TTSVoice.get(voice_id)
    
    async def get_by_name(self, name: str) -> Optional[TTSVoice]:
        """根据名称获取音色"""
        return await TTSVoice.find_one(TTSVoice.name == name)
    
    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[TTSVoice]:
        """获取音色列表"""
        voices = await TTSVoice.find_all().skip(skip).limit(limit).to_list()
        
        return voices
    
    async def create(self, voice: TTSVoiceCreate) -> TTSVoice:
        """创建音色"""
        # 转换字段名
        voice_data = voice.dict()
        voice_data['platform_id'] = voice_data.pop('platformId')
        voice_data['role_id'] = voice_data.pop('roleId')
        voice_data['extension_json'] = voice_data.pop('extensionJson')
        
        db_voice = TTSVoice(**voice_data)
        await db_voice.insert()
        return db_voice
    
    async def update(self, voice_id: str, voice: TTSVoiceUpdate) -> Optional[TTSVoice]:
        """更新音色"""
        db_voice = await self.get(voice_id)
        if db_voice:
            update_data = voice.dict(exclude_unset=True)
            # 转换字段名
            if 'platformId' in update_data:
                update_data['platform_id'] = update_data.pop('platformId')
            if 'roleId' in update_data:
                update_data['role_id'] = update_data.pop('roleId')
            if 'extensionJson' in update_data:
                update_data['extension_json'] = update_data.pop('extensionJson')
            
            await db_voice.update({"$set": update_data})
            db_voice.update_timestamp()
            await db_voice.save()
        return db_voice
    
    async def delete(self, voice_id: str) -> Optional[TTSVoice]:
        """删除音色"""
        db_voice = await self.get(voice_id)
        if db_voice:
            await db_voice.delete()
        return db_voice

    async def count(self) -> int:
        """统计音色总数"""
        return await TTSVoice.find_all().count()

# 创建CRUD实例
tts_voice_crud = TTSVoiceCRUD() 