from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.crud.tts_voice import tts_voice_crud
from app.schemas.tts_voice import TTSVoice, TTSVoiceCreate, TTSVoiceUpdate
from app.utils.response import success
from app.models.tts_platform import TTSPlatform

router = APIRouter()

@router.get("/voices")
async def get_voices(
    pageIndex: int = Query(1, alias="pageIndex"),
    pageSize: int = Query(10, alias="pageSize")
):
    """分页获取音色列表"""
    total = await tts_voice_crud.count()
    skip = (pageIndex - 1) * pageSize
    voices = await tts_voice_crud.get_multi(skip=skip, limit=pageSize)
    result = []
    for voice in voices:
        platform_name = None
        if voice.platform_id:
            platform = await TTSPlatform.get(voice.platform_id)
            if platform:
                platform_name = platform.name
        voice_dict = {
            "id": str(voice.id),
            "name": voice.name,
            "platformId": voice.platform_id,
            "platformName": platform_name,
            "roleId": voice.role_id,
            "status": voice.status,
            "extensionJson": voice.extension_json,
            "createTime": voice.created_at,
            "updateTime": voice.updated_at
        }
        result.append(voice_dict)
    return success({
        "total": total,
        "list": result
    })

@router.post("/voices")
async def create_voice(voice: TTSVoiceCreate):
    """创建音色"""
    db_voice = await tts_voice_crud.create(voice)
    return success({
        "id": str(db_voice.id),
        "name": db_voice.name,
        "platformId": db_voice.platform_id,
        "roleId": db_voice.role_id,
        "status": db_voice.status,
        "extensionJson": db_voice.extension_json,
        "createTime": db_voice.created_at,
        "updateTime": db_voice.updated_at
    })

@router.put("/voices/{voice_id}")
async def update_voice(voice_id: str, voice: TTSVoiceUpdate):
    """更新音色"""
    db_voice = await tts_voice_crud.update(voice_id, voice)
    if not db_voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    return success({
        "id": str(db_voice.id),
        "name": db_voice.name,
        "platformId": db_voice.platform_id,
        "roleId": db_voice.role_id,
        "status": db_voice.status,
        "extensionJson": db_voice.extension_json,
        "createTime": db_voice.created_at,
        "updateTime": db_voice.updated_at
    })

@router.delete("/voices/{voice_id}")
async def delete_voice(voice_id: str):
    """删除音色"""
    db_voice = await tts_voice_crud.delete(voice_id)
    if not db_voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    return success({"message": "Voice deleted successfully"}) 