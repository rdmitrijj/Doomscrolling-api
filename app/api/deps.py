from typing import Annotated
from fastapi import Depends
from app.db.db import Sessionlocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.doomscroll_db import DoomscrollingRepository
from app.services.doomservice import DoomscrollService


async def get_db():
    async with Sessionlocal() as db:
        yield db

db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def get_repo(db: db_dependency):
    return DoomscrollingRepository(db)

repo_dependency=  Annotated[DoomscrollingRepository, Depends(get_repo)]


async def get_service(repo: repo_dependency):
     return DoomscrollService(repo)

service_dependency = Annotated[DoomscrollService, Depends(get_service)]
