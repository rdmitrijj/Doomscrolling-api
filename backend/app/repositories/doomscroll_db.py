
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from ..models.tables import AppsTime
from ..schemas.schemas import InputSchema

import datetime

class DoomscrollingRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[AppsTime]:
        result = await self.db.scalars(select(AppsTime))
        return list(result.all())

    async def load_info(self, payload: InputSchema) -> None:
        self.db.add(AppsTime(**payload.model_dump()))
        await self.db.commit()

    async def calculate_avg_time(self, days: int):

        todays_date = datetime.date.today()
        start_date = todays_date - datetime.timedelta(days=days)

        result = await self.db.execute(
                    select(AppsTime.app, func.round(func.avg(AppsTime.seconds))
                            .label("seconds"))
                            .where(AppsTime.date >= start_date)
                            .group_by(AppsTime.app)
                            )
        return result

    async def calculate_all_time(self, days: int):
        todays_date = datetime.date.today()
        start_date = todays_date - datetime.timedelta(days=days)
    
        result = await self.db.execute(
            select(AppsTime.app, func.sum(AppsTime.seconds).label("seconds"))
            .where(AppsTime.date >= start_date)
            .group_by(AppsTime.app)
        )

        return result
    