import json
from http.client import responses
from typing import Optional

from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.service.error_responses import APIErrorResponse
from src.service.error_responses import InternalServerAPIError
from src.utils import format_pydantic_validation_error
from src.utils import http_headers
from src.utils.format_pydantic_validation_error import PydanticErrorResponseModel


async def custom_exception_handler(
        request: Request,
        error: Exception
):
    if not isinstance(error, APIErrorResponse):
        error = InternalServerAPIError()
    return await http_headers.add_response_headers(
        JSONResponse(
            status_code=error.to_status_code(),
            content=jsonable_encoder(
                {
                    "response": "NOK",
                    "error": {
                        "status_code": error.to_status_code(),
                        "code": error.to_code(),
                        "message": error.to_message()
                    }
                }
            )
        ), None
    )


def process_for_multipart_form_error(response_json: dict):
    if response_json.get('error', {}).get('message', '').find("Missing boundary in multipart..") > -1:
        response_json['error'][
            'message'] = 'The request is missing a file to be uploaded. Please attach a file in the body of the request'
    return response_json


async def custom_http_exception_handler(request, exc):
    response = await http_exception_handler(request, exc)
    try:
        _js = json.loads(response.body)
        if "response" not in _js and "code" not in _js and "status_code" not in _js:
            _js["response"] = "NOK"
            message = _js.pop("detail") + "."
            _js["error"] = {
                "status_code": response.status_code,
                "code": responses[
                    response.status_code].lower().replace(" ", "_"),
                "message": message
            }
            _js = process_for_multipart_form_error(_js)
            return JSONResponse(
                status_code=response.status_code,
                content=jsonable_encoder(_js)
            )
    except:
        pass
    return response


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    response = await request_validation_exception_handler(request, exc)
    error: Optional[PydanticErrorResponseModel]
    try:
        if error := format_pydantic_validation_error.execute(
                exc.errors()):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=jsonable_encoder(
                    {
                        "response": "NOK",
                        "error": {
                            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "code": error.code,
                            "message": error.message
                        }
                    }
                ),
            )
    except:
        pass
    return response
