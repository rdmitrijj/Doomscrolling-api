import datetime

from pydantic import BaseModel

class InputSchema(BaseModel):
    
    date: datetime.date
    app: str
    seconds: int

class OutputSchema(BaseModel):
    app: str
    seconds: int

class OutputSchemaDays(BaseModel):
    apps: list[OutputSchema]
    total: int

class DaysSchema(BaseModel):
    days: int