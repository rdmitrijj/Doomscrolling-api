from typing import Annotated
from sqlalchemy import select
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.tables import AppsTime
from ..schemas.schemas import InputSchema


class DoomscrollingRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[AppsTime]:
        result = await self.db.scalars(select(AppsTime))
        return list(result.all())

    async def load_info(self, payload: InputSchema) -> None:
        self.db.add(AppsTime(**payload.model_dump()))
        await self.db.commit()


async def get_repo(db):
    return DoomscrollingRepository(db)


repo_dependency=  Annotated[DoomscrollingRepository, Depends(get_repo)]