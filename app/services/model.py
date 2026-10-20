from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from err import NotFound
from models.aimodel import Ai_Model
from models.aimodelcap import Ai_Model_Cap
from models.aimodelprice import Ai_Model_Price
from models.provider import Provider
from schema.detail import Detail, AiProvider, AiModelBase, AiModelCap, AiModelPrice


class ModelService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_model_detail(self, id: int) -> Detail:
        # 列查询：只 SELECT schema 需要的列，不再 hydrate ORM 实体，selectinload 那三条额外
        # SELECT（provider / capabilities / prices）也就不需要了，顺带不再读 created_at、
        # updated_at、ai_model.status 这些 schema 用不到的列。
        #
        # provider.status 仍是"整条记录是否可见"的行级过滤：join 不上即视作不存在，走下面 404。
        # join 条件本身就是 id 相等，所以这里取 Ai_Model.provider_id 一列即可，它同时等于
        # Provider.id（AiProvider.id 直接复用它，避免和 Ai_Model.id 的 "id" 键撞名）。
        stmt = (
            select(
                Ai_Model.id,
                Ai_Model.model_slug,
                Ai_Model.display_name,
                Ai_Model.model_version,
                Ai_Model.model_family,
                Ai_Model.context_length_raw,
                Ai_Model.max_output_raw,
                Ai_Model.thinking_support,
                Ai_Model.default_thinking_mode,
                Ai_Model.thinking_note,
                Ai_Model.concurrency_limit,
                Ai_Model.doc_url,
                Ai_Model.description,
                Ai_Model.provider_id,
                Provider.provider_code,
                Provider.provider_name,
                Provider.website_url,
                Provider.status,
            )
            .join(Provider, Provider.id == Ai_Model.provider_id)
            .where(Ai_Model.id == id, Provider.status == 1)
        )
        row = (await self.db.execute(stmt)).first()

        if row is None:
            raise NotFound(f"模型不存在或所属供应商已停用: id={id}")

        # capabilities 的 is_active 跟上面 provider.status 是【两层】，不要拉平：provider.status
        # 决定这行记录可不可见（不可见 -> 404），is_active 只决定哪些子行出现在返回里，
        # 被过滤掉的子行不会导致 404。列查询下两者都只是普通 where，没有实体身份和写回问题。
        cap_rows = (
            await self.db.execute(
                select(
                    Ai_Model_Cap.id,
                    Ai_Model_Cap.cap_name,
                    Ai_Model_Cap.support_status,
                    Ai_Model_Cap.is_beta,
                    Ai_Model_Cap.is_active,
                    Ai_Model_Cap.note,
                ).where(Ai_Model_Cap.model_id == id, Ai_Model_Cap.is_active.is_(True))
            )
        ).all()

        price_rows = (
            await self.db.execute(
                select(
                    Ai_Model_Price.id,
                    Ai_Model_Price.price_type,
                    Ai_Model_Price.time_period,
                    Ai_Model_Price.price,
                ).where(Ai_Model_Price.model_id == id)
            )
        ).all()

        return Detail(
            provider=AiProvider(
                id=row.provider_id,
                provider_code=row.provider_code,
                provider_name=row.provider_name,
                website_url=row.website_url,
                status=row.status,
            ),
            model=AiModelBase.model_validate(dict(row._mapping)),
            capabilities=[AiModelCap.model_validate(dict(r._mapping)) for r in cap_rows],
            prices=[AiModelPrice.model_validate(dict(r._mapping)) for r in price_rows],
        )