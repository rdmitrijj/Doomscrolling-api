import datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.schemas.schemas import (
    InputSchema,
    DaysSchema,
    OutputSchemaDays, DateTimeSchema,
)
from app.api.deps import service_dependency


router = APIRouter(prefix="/load_user_info", tags=["user_info"])

@router.post("/doomscrolled_time",status_code=status.HTTP_201_CREATED,)
async def doomscrolled_time(service: service_dependency, payload: DaysSchema) -> OutputSchemaDays:
    # step 1 -if there any data in redis
    return await service.list_time(payload.days) # step 2 - if no, then go to redis
    # step 3 - save to cache if there no data in redis
    
@router.post(path="/average_wasted_time",status_code = status.HTTP_200_OK,)
async def calculate_avgtime(service: service_dependency, payload: DaysSchema) -> OutputSchemaDays:
    return await service.list_avg_time(payload.days)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def load_info(service: service_dependency, payload: InputSchema):
    try:
        await service.load_info(payload)
        # to invalidate cache - to be him actual
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="App with this name already loaded this day"
        )

@router.get("/doomscrolled_time/{date}", status_code=status.HTTP_200_OK)
async def doomscrolled_time_by_day(date: datetime.date, service: service_dependency):
    # to invalidate cache - to be him actual
    result = await service.get_by_day(date)
    return result

@router.delete("/doomscrolled_day_delete/{date}", status_code=status.HTTP_204_NO_CONTENT)
async def doomscroll_day_delete(service: service_dependency, date: datetime.date) -> None:
    await service.delete_day(date)