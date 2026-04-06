import uvicorn
from openenv.core.env_server import create_fastapi_app
from models import SQLAction, SQLObservation
from server.environment import SQLEnvironment

app = create_fastapi_app(SQLEnvironment, SQLAction, SQLObservation)

# This is the entry point the deployer is looking for!
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)
