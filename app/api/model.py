import logging

from fastapi import APIRouter, Depends, HTTPException,Query

from deps import get_model_service
from utils.responsed import AppError
from services.model import ModelService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/models", tags=["Models"])


@router.get("/")
async def get_model(
    id: int,
    service: ModelService = Depends(get_model_service)
):
    try:
        return await service.get_model_detail(id)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)



@router.get("/{provider_code}")
async def get_models_list(
    provider_code:str,
    page:int = Query(1,ge=1),
    size:int = Query(10,ge=1,le=100),
    service: ModelService = Depends(get_model_service)
):
    try:
        return await service.get_model_list(provider_code=provider_code,page=page,size=size)
    except AppError as e:
        raise HTTPException(status_code=e.status_code,detail=e.msg)