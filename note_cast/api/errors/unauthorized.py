from typing import Any, Union

from fastapi import status

from .custom_http_exc import CustomHTTPException


class InvalidCredentialsExc(CustomHTTPException):
    def __init__(
        self,
        detail: Union[str, None] = "Invalid credentials",
        headers: Union[dict, None] = {"WWW-Authenticate": "Bearer"},
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        category: Union[str, None] = None,
        errors: Any = None,
    ):
        super().__init__(
            headers=headers,
            status_code=status_code,
            detail=detail,
            category=category,
            errors=errors,
        )
