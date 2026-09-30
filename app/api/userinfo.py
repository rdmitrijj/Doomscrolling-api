
from fastapi import APIRouter, status
from app.schemas.schemas import InputSchema


router = APIRouter(
    prefix="/userinfo",
    tags=["userinfo"]
)

@router.get("/")
async def get_info(payload: InputSchema):
    return payload