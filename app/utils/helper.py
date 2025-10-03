import http
import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from utils.logger import logger
from models.base import GenericResponseModel


def build_api_response(generic_response: GenericResponseModel) -> JSONResponse:
    try:
        if not generic_response.api_id:
            generic_response.api_id = str(uuid.uuid4().hex)
        if not generic_response.status_code:
            generic_response.status_code = http.HTTPStatus.OK if not generic_response.error else http.HTTPStatus.UNPROCESSABLE_ENTITY
        response_json = jsonable_encoder(generic_response)
        res = JSONResponse(status_code=generic_response.status_code, content=response_json)
        logger.info(msg=f"build_api_response: Generated Response with status_code:{generic_response.status_code}")
        return res
    except Exception as e:
        logger.error(msg=f"exception in build_api_response error : {e}")
        return JSONResponse(status_code=generic_response.status_code, content=generic_response.error)
