from fastapi import APIRouter

from .provider import router as provider_router
from .model import router as model_router

service_router = APIRouter()

for r in (
    provider_router,
    model_router
):
    service_router.include_router(r)

__all__ = ["service_router"]