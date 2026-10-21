from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils import NotFound,info
from models import Provider
from schemas import to_index


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