from typing import Any, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from note_cast.schemas.responses import ApiErrorResponse
from starlette.requests import Request
from starlette.responses import JSONResponse


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        category: Union[str, None] = None,
        detail: Union[str, None] = None,
        errors: Any = None,
        headers: Union[dict, None] = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.category = category
        self.errors = errors
        self.headers = headers


async def http_error_handler(_: Request, exc: CustomHTTPException) -> JSONResponse:
    content = ApiErrorResponse(
        status_code=exc.status_code,
        detail=exc.detail,
    )

    if exc.category is not None:
        content.category = exc.category
    
    if exc.errors is not None:
        content.errors = exc.errors

    return JSONResponse(
        content=jsonable_encoder(content.dict(exclude_none=True)),
        status_code=exc.status_code, 
        headers=exc.headers
    )
