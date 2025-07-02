from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.crud.tts_platform import tts_platform_crud
from app.schemas.tts_platform import TTSPlatform, TTSPlatformCreate, TTSPlatformUpdate
from app.utils.response import success

router = APIRouter()

@router.get("/platforms")
async def get_platforms(
    pageIndex: int = Query(1, alias="pageIndex"),
    pageSize: int = Query(10, alias="pageSize")
):
    """分页获取平台列表"""
    total = await tts_platform_crud.count()
    skip = (pageIndex - 1) * pageSize
    page_platforms = await tts_platform_crud.get_multi(skip=skip, limit=pageSize)
    result = []
    for platform in page_platforms:
        platform_dict = {
            "id": str(platform.id),
            "name": platform.name,
            "type": platform.type,
            "status": platform.status,
            "config": platform.config,
            "createTime": platform.created_at,
            "updateTime": platform.updated_at
        }
        result.append(platform_dict)
    return success({
        "total": total,
        "list": result
    })

@router.post("/platforms", response_model=TTSPlatform)
async def create_platform(platform: TTSPlatformCreate):
    """创建平台"""
    return success(await tts_platform_crud.create(platform))

@router.put("/platforms/{platform_id}", response_model=TTSPlatform)
async def update_platform(platform_id: str, platform: TTSPlatformUpdate):
    """更新平台"""
    db_platform = await tts_platform_crud.update(platform_id, platform)
    if not db_platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return success(db_platform)

@router.delete("/platforms/{platform_id}")
async def delete_platform(platform_id: str):
    """删除平台"""
    db_platform = await tts_platform_crud.delete(platform_id)
    if not db_platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return success({"message": "Platform deleted successfully"}) 