from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from err import NotFound
from models.aimodel import Ai_Model
from schema.detail import Detail, AiProvider, AiModelBase, AiModelCap, AiModelPrice


class ModelService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_model_detail(self, id: int) -> Detail:
        query = (
            select(Ai_Model)
            .options(
                selectinload(Ai_Model.provider),
                selectinload(Ai_Model.capabilities),
                selectinload(Ai_Model.prices),
            )
            .where(Ai_Model.id == id)
        )
        result = await self.db.execute(query)
        m = result.scalars().first()

        if m is None:
            raise NotFound(f"模型不存在: id={id}")

        active_caps = [cap for cap in m.capabilities if cap.is_active]

        return Detail(
            provider=AiProvider.model_validate(m.provider),
            model=AiModelBase.model_validate(m),
            capabilities=[AiModelCap.model_validate(c) for c in active_caps],
            prices=[AiModelPrice.model_validate(p) for p in m.prices],
        )