import uvicorn
from openenv.core.env_server import create_fastapi_app
from models import SQLAction, SQLObservation
from server.environment import SQLEnvironment

app = create_fastapi_app(SQLEnvironment, SQLAction, SQLObservation)

# 1. The main function the deployer asked for
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)

# 2. The callable trigger the deployer asked for
if __name__ == "__main__":
    main()
