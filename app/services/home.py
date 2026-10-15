from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from err import NotFound
from models.provider import Provider
from schema import AmBase, AmBaseList


class HomeService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def index(
        self,
        page: int,
        size: int,
    ) -> AmBaseList:
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

        items = [
            AmBase(id=row.id, name=row.provider_name, ico=row.ico)
            for row in result
        ]
        return AmBaseList(items=items)