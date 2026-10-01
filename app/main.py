
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import userinfo
from contextlib import asynccontextmanager
from app.models.models import Base
from app.db.db import engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:8000"],
    allow_methods=["*"]
)


app.include_router(userinfo.router)
