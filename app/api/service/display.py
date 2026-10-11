import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from config.db import get_db
from model import Ai_Model,Provider
from schema import AiModelBase, AiModelCap, AiModelPrice, AiProvider, Detail, AmBase, AmBaseList

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/service/display", tags=["Display"])

#这个主要是渲染成厂商列表?
@router.get("/models", response_model=AmBaseList)
async def index(
    page : int = Query(1, ge=1),
    size : int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> AmBaseList:
    
    skip = (page - 1) * size
    query = await db.execute(
        select(Provider.id, Provider.provider_name, Provider.ico)
        .where(Provider.status == 1)
        .offset(skip)
        .limit(size)
    )
    result = query.all()
    items = [AmBase(id=row.id, name=row.provider_name, ico=row.ico if row.ico is not None else None) for row in result]
    return AmBaseList(items=items)


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


