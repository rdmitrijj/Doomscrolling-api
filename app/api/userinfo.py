from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.schemas.schemas import (
    InputSchema,
    DaysSchema,
    OutputSchema,
    OutputSchemaDays,
)
from ..repositories.doomscroll_db import repo_dependency

router = APIRouter(prefix="/load_user_info", tags=["user_info"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def load_info(payload: InputSchema, db: repo_dependency):

    try:
        await db.load_info(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=403, detail="App with this name already loaded this day"
        )

@router.post(
    "/average_spend_time",
    status_code=status.HTTP_201_CREATED,
    response_model=OutputSchemaDays,
)

async def calculate_avgtime(
    db: repo_dependency, payload: DaysSchema
) -> OutputSchemaDays:

    result = await db.calculate_avg_time(payload.days)
    
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

async def doomscrolled_time(db: repo_dependency, payload: DaysSchema):


    result = await db.calculate_all_time(payload.days)
    result = result.mappings().all()


    total = sum(row["seconds"] for row in result)
    apps = [OutputSchema(app=row["app"], seconds=row["seconds"]) for row in result]

    return OutputSchemaDays(apps=apps, total=total)


