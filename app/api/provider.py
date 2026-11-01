import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_model_service, get_provider_service
from utils.responsed import AppError
from services.model import ModelService
from services.provider import ProviderService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/providers", tags=["Providers"])


# 供应商列表
@router.get("")
async def list_providers(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    service: ProviderService = Depends(get_provider_service)
):
    try:
        return await service.list_providers(page=page, size=size)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)


# 供应商详情
@router.get("/{provider_code}")
async def get_provider(
    provider_code: str,
    service: ProviderService = Depends(get_provider_service)
):
    try:
        return await service.get_provider_detail(provider_code=provider_code)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)


# 该供应商的模型分页列表
@router.get("/{provider_code}/models")
async def get_provider_models(
    provider_code: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    service: ModelService = Depends(get_model_service)
):
    try:
        return await service.get_model_list(
            provider_code=provider_code,
            page=page,
            size=size,
        )
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)


# 首页用：供应商详情 + 最近 5 条模型
@router.get("/{provider_code}/overview")
async def get_provider_overview(
    provider_code: str,
    service: ProviderService = Depends(get_provider_service)
):
    try:
        return await service.get_overview(provider_code=provider_code)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)