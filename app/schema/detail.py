from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AiProvider(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    provider_code: str
    provider_name: str
    website_url: Optional[str] = None
    status: bool
    created_at: datetime
    updated_at: datetime


class AiModelBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    model_slug: str
    display_name: str
    model_version: Optional[str] = None
    model_family: Optional[str] = None

    context_length_raw: Optional[str] = None
    max_output_raw: Optional[str] = None

    thinking_support: str
    default_thinking_mode: Optional[str] = None
    thinking_note: Optional[str] = None

    concurrency_limit: Optional[int] = None
    status: str

    doc_url: Optional[str] = None
    description: Optional[str] = None

    provider_id: int

    created_at: datetime
    updated_at: datetime


class AiModelCap(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    cap_code: str
    cap_name: str
    support_status: str
    is_beta: bool
    note: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AiModelPrice(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    price_type: str
    time_period: str
    price: float
    created_at: datetime
    updated_at: datetime


class Detail(BaseModel):

    provider: AiProvider
    model: AiModelBase
    capabilities: list[AiModelCap]
    prices: list[AiModelPrice]


# ---- 分页响应 ----

class ModelListResponse(BaseModel):

    items: list[AiModelBase]
    total: int
    page: int
    page_size: int


class ProviderListResponse(BaseModel):

    items: list[AiProvider]
    total: int
    page: int
    page_size: int


class ProviderDetailResponse(BaseModel):

    provider: AiProvider
    models: list[AiModelBase]