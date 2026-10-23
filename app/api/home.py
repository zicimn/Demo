import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_home_service
from utils.responsed import AppError
from services.home import HomeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/home", tags=["Home"])


#这个主要是渲染成厂商列表?
@router.get("/")
async def index(
    page : int = Query(1, ge=1),
    size : int = Query(20, ge=1, le=100),
    service: HomeService = Depends(get_home_service)
):
    try:
        return await service.index(page=page, size=size)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)


@router.get("/models/{provider_code}")
async def index(
    provider_code:str,
    service: HomeService = Depends(get_home_service)
):
    try:
        return await service.details(provider_code=provider_code)
    except AppError as e:
        raise HTTPException(status_code=e.status_code,detail=e.msg)