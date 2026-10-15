from fastapi import APIRouter

from .home import router as home_router
from .model import router as model_router

service_router = APIRouter()

for r in (
    home_router,
    model_router
):
    service_router.include_router(r)

__all__ = ["service_router"] 
