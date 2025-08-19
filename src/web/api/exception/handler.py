from contextlib import suppress

import fastapi
import starlette
from fastapi.requests import Request
from starlette.responses import JSONResponse

from src.utility import APIErrorSpecs, StatusCodeMap
from src.web.api.exception.model import APIException
from src.web.schema.common import ErrorSO, ResponseSO


async def exception_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR

    if isinstance(exception, APIException):
        error = exception.error_so
    else:
        error = ErrorSO(
            error=StatusCodeMap(status_code).name,
            error_code=APIErrorSpecs.unknown_error,
            error_data={
                "exception_type": str(type(exception)),
                "exception_str": str(exception),
                "request.method": str(request.method),
                "request.url": str(request.url),
            },
        )

    if isinstance(exception, APIException):
        status_code = exception.status_code

    elif isinstance(exception, starlette.exceptions.HTTPException):
        status_code = (
            exception.status_code
            if exception.status_code in StatusCodeMap
            else fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        with suppress(Exception):
            error.error_data["exception.detail"] = exception.detail


    elif isinstance(exception, fastapi.exceptions.RequestValidationError):
        status_code = fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY

        with suppress(Exception):
            error.error_data["exception.errors"] = (
                str(exception.errors()) if exception.errors() else {}
            )
    else:
        status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR

    error.error = StatusCodeMap(status_code).name
    error.error_data["status_code"] = status_code

    return JSONResponse(
		content=ResponseSO(payload=None, error=error).model_dump(mode="json", fallback=str),
		status_code=status_code
    )


def apply_exception_handler(app: fastapi.FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.RequestValidationError,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.HTTPException,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=starlette.exceptions.HTTPException,
        handler=exception_handler
    )
