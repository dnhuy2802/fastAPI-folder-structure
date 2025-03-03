import os

class CoreCFG:
    APP_PORT = int(os.environ.get('APP_PORT', 8000))
    PROJECT_NAME = "FastAPI Project"