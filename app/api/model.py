import logging

from fastapi import APIRouter, Depends, HTTPException

from deps import get_model_service
from utils.responsed import AppError
from services.model import ModelService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/models", tags=["Models"])


# 模型详情，路径参数统一用模型 id
@router.get("/{model_id}")
async def get_model_detail(
    model_id: int,
    service: ModelService = Depends(get_model_service)
):
    try:
        return await service.get_model_detail(model_id)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)