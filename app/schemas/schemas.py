from pydantic import BaseModel
import datetime



class InputSchema(BaseModel):
    
    date: datetime.date
    app: str
    seconds: int

class OutputSchema(BaseModel):
    date: datetime.date
    app: str
    seconds: int