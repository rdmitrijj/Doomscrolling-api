import datetime

from pydantic import BaseModel

class InputSchema(BaseModel):
    
    date: datetime.date
    app: str
    seconds: int

class OutputSchemaAvgDays(BaseModel):
    app: str
    seconds: int

class OutputSchemaSumDays(BaseModel):
    apps: list[OutputSchemaAvgDays]
    total: int

class DaysSchema(BaseModel):
    days: int