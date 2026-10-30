from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils import NotFound, info
from models import Provider
from schemas import to_provider


class ProviderService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_providers(
        self,
        page: int,
        size: int,
    ):
        skip = (page - 1) * size
        query = await self.db.execute(
            select(Provider)
            .where(Provider.status == 1)
            .order_by(Provider.id)
            .offset(skip)
            .limit(size)
        )

        result = query.scalars().all()
        if not result:
            raise NotFound("展示列表为空")

        items = [to_provider(row) for row in result]
        return info(data=items)

    # 供应商详情：原来只是 HomeService.get_id 的内部方法，现在单独暴露成接口
    async def get_provider_detail(
        self,
        provider_code: str
    ):
        provider = await self._get_enabled_provider(provider_code)
        return info(data=to_provider(provider))

    # 首页用：供应商详情 + 最近 5 条模型。
    # 前 5 条模型与 /api/providers/{provider_code}/models 有重叠，保留是为了首页少一次请求。
    async def get_overview(
        self,
        provider_code: str
    ):
        from .model import ModelService

        provider = await self._get_enabled_provider(provider_code)

        mod = ModelService(db=self.db)
        mod_data = (
            await mod.get_model_list(
                provider_code=provider_code,
                page=1,
                size=5,
            )
        ).get("data").get("models_data")

        data = {
            "provider": to_provider(provider),
            "models_data": mod_data,
        }
        return info(data=data)

    # 按 provider_code 取启用的供应商，找不到直接抛 NotFound
    async def _get_enabled_provider(
        self,
        provider_code: str
    ) -> Provider:
        query = await self.db.execute(
            select(Provider)
            .where(Provider.status == 1)
            .where(Provider.provider_code == provider_code)
        )

        provider = query.scalar_one_or_none()
        if not provider:
            raise NotFound(f"供应商不存在或已停用: provider_code={provider_code}")
        return provider