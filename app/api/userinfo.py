
from fastapi import APIRouter, status
from app.schemas.schemas import InputSchema
from ..db.db import db_dependency
from ..models.models import AppsTime


router = APIRouter(
    prefix="/userinfo",
    tags=["userinfo"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def load_info(payload: InputSchema, db: db_dependency):

    new_info = AppsTime(**payload.model_dump())
    db.add(new_info)
    await db.commit()

    return {"Info":"was successfully added"}
