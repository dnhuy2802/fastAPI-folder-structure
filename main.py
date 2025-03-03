import http
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from logs import logger
from config.config import CoreCFG
from src.controllers import status


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

app = FastAPI()
app.title = f"{CoreCFG.PROJECT_NAME}"
app.version = "0.0.1"

app.include_router(status.status_router)

# Create a GET method that responds with HTML code
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Welcome to SHIV PPS Planning Optimization API Services</h1>')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CoreCFG.APP_PORT)