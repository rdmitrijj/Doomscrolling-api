
from fastapi import APIRouter, status, HTTPException
from app.schemas.schemas import InputSchema, DaysSchema, OutputSchemaAvgDays, OutputSchemaSumDays
from ..db.db import db_dependency
from ..models.models import AppsTime
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

import datetime

router = APIRouter(
    prefix="/user_info",
    tags=["user_info"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def load_info(payload: InputSchema, db: db_dependency):

    new_info = AppsTime(**payload.model_dump())
    try:
        db.add(new_info)
        await db.commit()
        return "success"
    except IntegrityError:
        raise HTTPException(status_code=403, detail="App with this name already loaded this day")

    
@router.post("/average_time", status_code=status.HTTP_201_CREATED, response_model=list[OutputSchemaAvgDays])
async def calculate_avgtime(db: db_dependency, payload: DaysSchema):

    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(days=payload.days)

    result = await db.execute(select(AppsTime.app, func.round(func.avg(AppsTime.seconds), 0).label("seconds"))
                              .where(AppsTime.date >= start_date)
                              .group_by(AppsTime.app))
    result = result.all()

    return result

@router.post("/doomscrolled_time", status_code=status.HTTP_201_CREATED, response_model=OutputSchemaSumDays)
async def doomscrolled_time(db: db_dependency, payload: DaysSchema):

    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(days=payload.days)

    result = await db.execute(select(AppsTime.app, func.sum(AppsTime.seconds).label("seconds"))
                                  .where(AppsTime.date >= start_date)
                                  .group_by(AppsTime.app))
    result = result.mappings().all()

    total = sum(row["seconds"] for row in result)
    return OutputSchemaSumDays(apps=result, total=total)