
from fastapi import FastAPI
from app.api import userinfo


app = FastAPI()

app.include_router()