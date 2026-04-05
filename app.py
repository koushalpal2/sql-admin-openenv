import os
os.environ["ENABLE_WEB_INTERFACE"] = "true"

from openenv.core.env_server import create_web_interface_app
from models import Action, Observation
from server.environment import Environment

# Pass the Environment CLASS directly to the server
app = create_web_interface_app(Environment, Action, Observation)