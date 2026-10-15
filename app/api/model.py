import logging

from fastapi import APIRouter, Depends, HTTPException

from deps import get_model_service
from err import AppError
from schema.detail import Detail
from services.model import ModelService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/models", tags=["Models"])


@router.get("/{id}", response_model=Detail)
async def get_model(
    id: int,
    service: ModelService = Depends(get_model_service)
) -> Detail:
    try:
        return await service.get_model_detail(id)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)