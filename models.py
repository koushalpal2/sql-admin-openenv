from typing import Optional
from openenv.core.env_server import Action, Observation, State

class SQLAction(Action):
    sql_query: str

class SQLObservation(Observation):
    result: str
    error: Optional[str] = None
    reward: float = 0.0
    done: bool = False

class SQLState(State):
    current_task: int = 1
    step_count: int = 0
