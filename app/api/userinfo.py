from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.schemas.schemas import (
    InputSchema,
    DaysSchema,
    OutputSchema,
    OutputSchemaDays,
)
from ..db.db import db_dependency
from ..models.tables import AppsTime
from ..repositories.domscrollinfo import repo_dependency

import datetime

router = APIRouter(prefix="/user_info", tags=["user_info"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def load_info(payload: InputSchema, db: repo_dependency):

    try:
        await db.load_info(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=403, detail="App with this name already loaded this day"
        )

@router.post(
    "/average_time",
    status_code=status.HTTP_201_CREATED,
    response_model=OutputSchemaDays,
)
async def calculate_avgtime(
    db: db_dependency, payload: DaysSchema
) -> OutputSchemaDays:

    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(days=payload.days)

    result = await db.execute(
        select(AppsTime.app, func.round(func.avg(AppsTime.seconds), 0).label("seconds"))
        .where(AppsTime.date >= start_date)
        .group_by(AppsTime.app)
    )
    result = result.mappings().all()

    total = 0
    counter = 0
    for row in result:
        counter += 1
        total += row["seconds"]

    average = round(total/counter)
    apps = [OutputSchema(app=row["app"], seconds=row["seconds"]) for row in result]


    return OutputSchemaDays(apps=apps, total=average)


@router.post(
    "/doomscrolled_time",
    status_code=status.HTTP_201_CREATED,
    response_model=OutputSchemaDays,
)
async def doomscrolled_time(db: db_dependency, payload: DaysSchema):

    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(days=payload.days)

    result = await db.execute(
        select(AppsTime.app, func.sum(AppsTime.seconds).label("seconds"))
        .where(AppsTime.date >= start_date)
        .group_by(AppsTime.app)
    )
    result = result.mappings().all()
    total = sum(row["seconds"] for row in result)
    apps = [OutputSchema(app=row["app"], seconds=row["seconds"]) for row in result]

    return OutputSchemaDays(apps=apps, total=total)


