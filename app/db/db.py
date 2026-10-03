from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)

Sessionlocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with Sessionlocal() as db:
        yield db


db_dependency = Annotated[AsyncSession, Depends(get_db)]
