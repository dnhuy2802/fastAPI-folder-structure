import http
import json

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from contextlib import asynccontextmanager

from logs import logger

# register startup and shutdown using lifespan Events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup event
    logger.info("Startup Event Triggered")
    print("Startup Event Triggered")
    
    yield

    # shutdown event
    logger.info("Shutdown Event Triggered")
    # mongodb_client.close()
    # qdrant_client.close()
    print("Shutdown Event Triggered")

app = FastAPI()
app.title = "Name of Project"
app.version = "0.0.1"

# Create a GET method that responds with HTML code
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Welcome to Name of Project API Services</h1>')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)