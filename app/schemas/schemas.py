import datetime

from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    
    date: datetime.date
    app: str
    seconds: int

class OutputSchema(BaseModel):
    app: str
    seconds: int

class OutputSpecialDaySchema(BaseModel):
    app: str
    seconds: int
    date: datetime.date

class OutputSchemaDays(BaseModel):
    apps: list[OutputSchema]
    total: int

class DaysSchema(BaseModel):
    days: int = Field(gt=0)

class DateTimeSchema(BaseModel):
    date: datetime.date