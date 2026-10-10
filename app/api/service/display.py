import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from config.db import get_db
from model import Ai_Model
from schema import AiModelBase, AiModelCap, AiModelPrice, AiProvider, Detail

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/service/display", tags=["Display"])


@router.get("/models/{id}", response_model=Detail)
async def get_model(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Detail:
    query = (
        select(Ai_Model)
        .options(
            selectinload(Ai_Model.provider),
            selectinload(Ai_Model.capabilities),
            selectinload(Ai_Model.prices),
        )
        .where(Ai_Model.id == id)
    )
    result = await db.execute(query)
    m = result.scalars().first()

    if m is None:
        logger.warning("get_model: model not found, id=%d", id)
        raise HTTPException(status_code=404, detail="模型不存在")

    active_caps = [cap for cap in m.capabilities if cap.is_active]
    now = datetime.now(timezone.utc)
    valid_prices = [p for p in m.prices]

    logger.info(
        "get_model: id=%d slug='%s' caps=%d prices=%d",
        m.id,
        m.model_slug,
        len(active_caps),
        len(valid_prices),
    )

    return Detail(
        provider=AiProvider.model_validate(m.provider),
        model=AiModelBase.model_validate(m),
        capabilities=[AiModelCap.model_validate(c) for c in active_caps],
        prices=[AiModelPrice.model_validate(p) for p in valid_prices],
    )