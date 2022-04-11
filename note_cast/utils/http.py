from functools import lru_cache
from typing import Union

import httpx
from httpx import ConnectTimeout, HTTPStatusError, Response
from note_cast.schemas.responses import ApiErrorResponse
from pydantic import HttpUrl


def raise_on_4xx_5xx(response: Response):
    response.raise_for_status()


def httpx_client_factory(base_url: HttpUrl = None, **kwargs):
    httpx_client = httpx.Client(
        http2=True, event_hooks={"response": [raise_on_4xx_5xx]}
    )

    if base_url is not None:
        httpx_client.base_url = base_url

    if (headers := kwargs.get("headers", None)) is not None:
        httpx_client.headers = headers

    return httpx_client



@lru_cache
def get_default_client():
    return httpx_client_factory()


httpx_client = get_default_client()


def get_redirect_dest_url_proxy(initial_url: str) -> Union[str, ApiErrorResponse]:
    
    client = httpx_client_factory()
    with client:

        redirect_check_base_url = "https://prod.sureoakdata.com/api/v1/redirect-checker"
        params = {"initialURL": initial_url}

        try:
            r = client.post(redirect_check_base_url, params=params)
            destination_url = r.json().get("redirects")[-1].get("thisUrl")

            return destination_url

        except HTTPStatusError as exc:
            return ApiErrorResponse(
                category="http_client_error",
                message=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.",
            )

        except ConnectTimeout as exc:
            return ApiErrorResponse(
                category="connection_time_out",
                message="Failed to establish a connection.",
            )
