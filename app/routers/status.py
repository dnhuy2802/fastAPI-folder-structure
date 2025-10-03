import http
from fastapi import APIRouter
 
from models.base import GenericResponseModel
from utils.helper import build_api_response
 
status_router = APIRouter(tags=["status"])
 
@status_router.get('/health', tags=['status'], response_model=GenericResponseModel)
def health():
    """
    Health check endpoint to verify if the API is running correctly
    """
    res = GenericResponseModel(
        message="Service is up and running",
        data={"status": "healthy"},
        status_code=http.HTTPStatus.OK
    )
    return build_api_response(res)
