from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils import NotFound,info
from models import Provider,Ai_Model
from schemas import to_index,to_pdetail,to_detail
from typing import Optional,TYPE_CHECKING


class HomeService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def index(
        self,
        page: int,
        size: int,
    ):
        skip = (page - 1) * size
        query = await self.db.execute(
            select(Provider.id, Provider.provider_name, Provider.ico)
            .where(Provider.status == 1)
            .order_by(Provider.id)
            .offset(skip)
            .limit(size)
        )

        result = query.all()
        if not result:
            raise NotFound("展示列表为空")

        items = [ to_index(row) for row in result]
        return info(data=items)

    #内部获取id函数和信息
    async def get_id(
        self,
        provider_code:str
    ):
        query = await self.db.execute(
            select(Provider)
            .where(Provider.status == 1)
            .where(Provider.provider_code == provider_code)
        )
        
        result = query.scalar_one_or_none()
        if not result:
            raise NotFound("展示为空")

        return info(data=to_pdetail(result))

    
    #要将厂家+模型表同时起只显示最近5条
    async def details(
        self,
        provider_code:str
    ):  
        from .model import ModelService

        provider_data = await self.get_id(provider_code=provider_code)
        provider_id = provider_data.get("id")

        mod = ModelService(db=self.db)
        mod_data = (await mod.get_model_list(
            provider_code=provider_code,
            provider_id=provider_id,
            page=1,size=5
        )).get("data").get("models_data")

        data = {
            "provider_data":provider_data,
            "models_data": mod_data
        }
        return info(data=data)
        
        


    
