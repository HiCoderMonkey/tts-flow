from typing import List
from fastapi import APIRouter, Depends, status, Request, Query
from app.api.deps import get_current_active_user
from app.models.tts_flow import TTSFlow
from app.schemas.tts_flow import TTSFlow as TTSFlowSchema, TTSFlowCreate, TTSFlowUpdate
from app.services.tts_flow_service import TTSFlowService
from app.utils.response import success

router = APIRouter(prefix="/tts-flows", tags=["TTS工作流"])


@router.post("")
async def create_tts_flow(
    tts_flow_create: TTSFlowCreate,
    request: Request
):
    """创建TTS工作流"""
    current_user = await get_current_active_user(request)
    tts_flow = await TTSFlowService.create_tts_flow(tts_flow_create)
    return success(tts_flow.dict())


@router.get("")
async def read_tts_flows(
    request: Request,
    pageIndex: int = Query(1, alias="pageIndex"),
    pageSize: int = Query(10, alias="pageSize"),
    name: str = Query(None, description="按名称搜索")
):
    """分页获取TTS工作流列表"""
    current_user = await get_current_active_user(request)
    skip = (pageIndex - 1) * pageSize
    limit = pageSize
    if name:
        total = await TTSFlow.find({"name": {"$regex": name, "$options": "i"}}).count()
        tts_flows = await TTSFlowService.search_tts_flows(name=name, skip=skip, limit=limit)
    else:
        total = await TTSFlowService.get_tts_flows_total()
        tts_flows = await TTSFlowService.get_tts_flows(skip=skip, limit=limit)
    return success({
        "total": total,
        "list": [tts_flow.dict() for tts_flow in tts_flows]
    })


@router.get("/{flow_id}", response_model=TTSFlowSchema)
async def read_tts_flow(
    flow_id: str,
    request: Request
):
    """获取指定TTS工作流信息"""
    current_user = await get_current_active_user(request)
    tts_flow = await TTSFlowService.get_tts_flow_by_id(flow_id)
    return success(tts_flow.dict())


@router.put("/{flow_id}", response_model=TTSFlowSchema)
async def update_tts_flow(
    flow_id: str,
    tts_flow_update: TTSFlowUpdate,
    request: Request
):
    """更新指定TTS工作流信息"""
    current_user = await get_current_active_user(request)
    updated_flow = await TTSFlowService.update_tts_flow(flow_id, tts_flow_update)
    return success(updated_flow.dict())


@router.delete("/{flow_id}")
async def delete_tts_flow(
    flow_id: str,
    request: Request
):
    """删除TTS工作流"""
    current_user = await get_current_active_user(request)
    await TTSFlowService.delete_tts_flow(flow_id)
    return success({"message": "TTS工作流删除成功"})


@router.get("/search/name/{name}", response_model=TTSFlowSchema)
async def search_tts_flow_by_name(
    name: str,
    request: Request
):
    """根据名称搜索TTS工作流"""
    current_user = await get_current_active_user(request)
    tts_flow = await TTSFlowService.get_tts_flow_by_name(name)
    return success(tts_flow.dict()) 