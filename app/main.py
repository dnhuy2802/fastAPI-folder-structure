import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from utils.logger import logger
from config import CoreCFG
from routers.status import status_router


# register startup and shutdown using lifespan Events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup event
    logger.info("Startup Event Triggered")
    print("Startup Event Triggered")
    
    yield

    # shutdown event
    logger.info("Shutdown Event Triggered")
    print("Shutdown Event Triggered")

app = FastAPI(
    title=f"{CoreCFG.app_name}",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(status_router)

# Create a GET method that responds with HTML code
@app.get('/', tags = ['home'])
def message():
    return {
        "message": f"{CoreCFG.app_name} API Services",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=CoreCFG.app_host, port=CoreCFG.app_port, reload=CoreCFG.debug)