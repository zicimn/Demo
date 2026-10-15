from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_db
from services import HomeService, ModelService


async def get_model_service(
    db: AsyncSession = Depends(get_db)
) -> ModelService:
    return ModelService(db)


async def get_home_service(
    db: AsyncSession = Depends(get_db)
) -> HomeService:
    return HomeService(db)