import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_home_service
from err import AppError
from schema import AmBaseList
from services.home import HomeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/home", tags=["Home"])


#这个主要是渲染成厂商列表?
@router.get("/", response_model=AmBaseList)
async def index(
    page : int = Query(1, ge=1),
    size : int = Query(20, ge=1, le=100),
    service: HomeService = Depends(get_home_service)
) -> AmBaseList:
    try:
        return await service.index(page=page, size=size)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)