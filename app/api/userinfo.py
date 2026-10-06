from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.schemas.schemas import (
    InputSchema,
    DaysSchema,
    OutputSchemaDays,
)
from app.api.deps import service_dependency


router = APIRouter(prefix="/load_user_info", tags=["user_info"])

@router.post("/doomscrolled_time",status_code=status.HTTP_201_CREATED,)
async def doomscrolled_time(service: service_dependency, payload: DaysSchema) -> OutputSchemaDays:
    return await service.list_time(payload.days)
    
@router.post(path="/average_wasted_time",status_code = status.HTTP_200_OK,)
async def calculate_avgtime(service: service_dependency, payload: DaysSchema) -> OutputSchemaDays:

    return await service.list_avg_time(payload.days)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def load_info(service: service_dependency, payload: InputSchema):
    try:
        await service.load_info(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="App with this name already loaded this day"
        )

