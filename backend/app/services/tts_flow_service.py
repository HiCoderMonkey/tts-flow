from typing import List, Optional
from app.models.tts_flow import TTSFlow
from app.schemas.tts_flow import TTSFlowCreate, TTSFlowUpdate
from app.core.exceptions import (
    BusinessException,
    NotFoundException,
    ConflictException,
    ErrorCode
)


class TTSFlowService:
    """TTS工作流服务"""
    
    @staticmethod
    async def create_tts_flow(tts_flow_create: TTSFlowCreate) -> TTSFlow:
        """创建TTS工作流"""
        # 检查名称是否已存在
        existing_flow = await TTSFlow.find_one({"name": tts_flow_create.name})
        if existing_flow:
            raise BusinessException(
                message="工作流名称已存在",
                code=ErrorCode.RESOURCE_ALREADY_EXISTS
            )
        
        # 创建新工作流
        tts_flow = TTSFlow(
            name=tts_flow_create.name,
            flow_config=tts_flow_create.flow_config
        )
        
        await tts_flow.insert()
        return tts_flow
    
    @staticmethod
    async def get_tts_flow_by_id(flow_id: str) -> Optional[TTSFlow]:
        """根据ID获取TTS工作流"""
        tts_flow = await TTSFlow.get(flow_id)
        if not tts_flow:
            raise NotFoundException(
                message="TTS工作流不存在",
                code=ErrorCode.RESOURCE_NOT_FOUND
            )
        return tts_flow
    
    @staticmethod
    async def get_tts_flow_by_name(name: str) -> Optional[TTSFlow]:
        """根据名称获取TTS工作流"""
        tts_flow = await TTSFlow.find_one({"name": name})
        if not tts_flow:
            raise NotFoundException(
                message="TTS工作流不存在",
                code=ErrorCode.RESOURCE_NOT_FOUND
            )
        return tts_flow
    
    @staticmethod
    async def update_tts_flow(flow_id: str, tts_flow_update: TTSFlowUpdate) -> Optional[TTSFlow]:
        """更新TTS工作流"""
        tts_flow = await TTSFlow.get(flow_id)
        if not tts_flow:
            raise NotFoundException(
                message="TTS工作流不存在",
                code=ErrorCode.RESOURCE_NOT_FOUND
            )
        
        update_data = tts_flow_update.dict(exclude_unset=True)
        
        # 检查名称唯一性
        if "name" in update_data:
            existing_flow = await TTSFlow.find_one({"name": update_data["name"]})
            if existing_flow and existing_flow.id != flow_id:
                raise ConflictException(
                    message="工作流名称已存在",
                    code=ErrorCode.RESOURCE_ALREADY_EXISTS
                )
        
        # 更新工作流
        await tts_flow.update({"$set": update_data})
        tts_flow.update_timestamp()
        await tts_flow.save()
        
        return tts_flow
    
    @staticmethod
    async def delete_tts_flow(flow_id: str) -> bool:
        """删除TTS工作流"""
        tts_flow = await TTSFlow.get(flow_id)
        if not tts_flow:
            raise NotFoundException(
                message="TTS工作流不存在",
                code=ErrorCode.RESOURCE_NOT_FOUND
            )
        
        await tts_flow.delete()
        return True
    
    @staticmethod
    async def get_tts_flows(skip: int = 0, limit: int = 100) -> List[TTSFlow]:
        """获取TTS工作流列表"""
        return await TTSFlow.find_all().skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def search_tts_flows(name: str = None, skip: int = 0, limit: int = 100) -> List[TTSFlow]:
        """搜索TTS工作流"""
        query = {}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        
        return await TTSFlow.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_tts_flows_total() -> int:
        return await TTSFlow.count() 