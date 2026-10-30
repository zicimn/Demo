from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Ai_Model,Ai_Model_Cap,Ai_Model_Price,Provider
from schemas import to_model,to_model_capabilites,to_model_prices,to_provider,to_detail
from utils import info,NotFound


class ModelService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_model_detail(self, id: int) -> dict:

        stmt = (
            select(Ai_Model,Provider)
            .join(Provider,Provider.id == Ai_Model.provider_id)
            .where(Ai_Model.id == id,Provider.status == 1)
        )

        row = (await self.db.execute(stmt)).one_or_none()
        if row is None:
            raise NotFound(f"模型不存在或所属供应商已停用: id={id}")
        else:
            model_result,provider_result = row

        capabilities_reult = (
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

        prices_result = (
            await self.db.execute(
                select(
                    Ai_Model_Price.id,
                    Ai_Model_Price.price_type,
                    Ai_Model_Price.time_period,
                    Ai_Model_Price.price,
                ).where(Ai_Model_Price.model_id == id)
            )
        ).all()

        model = to_model(model_result)
        provider = to_provider(provider_result)
        capabilities = [ to_model_capabilites(c) for c in capabilities_reult]
        prices = [ to_model_prices(p) for p in prices_result]

        data = to_detail(model=model,proivder=provider,capabilities=capabilities,prices=prices)
        return info(data=data)


    # 供应商模型列表：只接受 provider_code 一个入口，provider_id 由这里统一解析
    async def get_model_list(
        self,
        provider_code:str,
        page:int,
        size:int,
    ):
        pid = (
            await self.db.execute(
                select(Provider.id).where(
                    Provider.provider_code == provider_code,
                    Provider.status == 1,
                )
            )
        ).scalar_one_or_none()

        if pid is None:
            raise NotFound(f"供应商不存在或已停用: provider_code={provider_code}")

        skip = (page - 1)*size
        mquery = await self.db.execute(
            select(Ai_Model)
            .where(Ai_Model.status == "active")
            .where(Ai_Model.provider_id == pid)
            .order_by(Ai_Model.publish_at.desc())#因为表还没填
            # .order_by(Ai_Model.created_at.desc())#暂时替代
            .offset(skip)
            .limit(size)
        )
        models = mquery.scalars().all()

        data = {"models_data":[to_model(m) for m in models]}
        return info(data=data)