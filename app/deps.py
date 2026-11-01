from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_db
from services import ProviderService, ModelService


async def get_model_service(
    db: AsyncSession = Depends(get_db)
) -> ModelService:
    return ModelService(db)


async def get_provider_service(
    db: AsyncSession = Depends(get_db)
) -> ProviderService:
    return ProviderService(db)