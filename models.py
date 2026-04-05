from pydantic import BaseModel
from typing import Optional

class Action(BaseModel):
    sql_query: str

class Observation(BaseModel):
    result: str
    error: Optional[str] = None
    reward: float = 0.0
    done: bool = False
    episode_id: str = "default-session"

# Add this new block so the server has an object instead of a dict!
class State(BaseModel):
    current_task: int
    step_count: int
    episode_id: str