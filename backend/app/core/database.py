from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.tts_flow import TTSFlow


async def init_db():
    """初始化数据库连接"""
    # 创建MongoDB客户端
    client = AsyncIOMotorClient(settings.mongodb_url)
    
    # 初始化Beanie
    await init_beanie(
        database=client[settings.database_name],
        document_models=[User, TTSFlow]
    )


async def close_db():
    """关闭数据库连接"""
    # Beanie会自动管理连接，这里可以添加清理逻辑
    pass 