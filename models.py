from pydantic import BaseModel
from typing import Optional

class Action(BaseModel):
    sql_query: str

class Observation(BaseModel):
    result: str
    error: Optional[str] = None
