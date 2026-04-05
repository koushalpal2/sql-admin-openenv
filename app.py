from openenv.core.env_server import create_fastapi_app
from models import Action, Observation
from server.environment import Environment

# Notice we use create_fastapi_app instead of the web_interface version
app = create_fastapi_app(Environment, Action, Observation)
