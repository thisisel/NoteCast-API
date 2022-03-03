from typing import Union
import httpx
from httpx import ConnectTimeout, HTTPStatusError, Response
from note_cast.schemas.response import ApiErrorResponse


def raise_on_4xx_5xx(response: Response):
    response.raise_for_status()


httpx_client = httpx.Client(http2=True, event_hooks={"response": [raise_on_4xx_5xx]})


def get_redirect_dest_url(initial_url: str) -> Union[str, ApiErrorResponse]:
    with httpx_client:

        redirect_check_base_url = "https://prod.sureoakdata.com/api/v1/redirect-checker"
        params = {"initialURL": initial_url}

        try:
            r = httpx_client.post(redirect_check_base_url, params=params)
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
