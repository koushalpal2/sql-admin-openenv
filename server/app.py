from openenv.core.env_server import create_fastapi_app
from models import SQLAction, SQLObservation
from server.environment import SQLEnvironment

# Pass the CLASS directly to the server, do not instantiate it first!
app = create_fastapi_app(SQLEnvironment, SQLAction, SQLObservation)
