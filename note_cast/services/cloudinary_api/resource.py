from typing import Literal

import cloudinary.api
from cloudinary.exceptions import Error
from fastapi import HTTPException
from httpx import HTTPError, Response
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.utils.http import httpx_client


class CloudinaryResource:

    RESOURCE_TYPE = Literal["image", "video", "raw"]

    @classmethod
    def get_resource_info(cls, public_id: str, resource_type: RESOURCE_TYPE):
        try:
            return cloudinary.api.resource(
                public_id=public_id, resource_type=resource_type
            )
        except Exception as exc:
            loguru_app_logger.exception(exc)

    # TODO move to tasks
    @classmethod
    def download_resource(cls, url):
        try:

            with httpx_client as client:

                r: Response = client.get(url)

                if r.status_code == 200:
                    return r
                else:
                    raise HTTPError

        except HTTPError as exc:
            loguru_app_logger.exception(f"HTTP Exception for {exc.request.url} - {exc}")

        except Exception as exc:
            loguru_app_logger.exception(exc)
            raise HTTPException(status_code=500)

    @classmethod
    def fetch_transcript(cls, public_id: str, resource_type: str = "raw"):

        try:
            resource_info_response = cls.get_resource_info(
                public_id=public_id, resource_type="raw"
            )
            resource_data = cls.download_resource(resource_info_response["url"])
            resource_data_jsn = resource_data.json()
            transcript = resource_data_jsn[0]["transcript"]
       
        except Error as err:
            loguru_app_logger.exception(err)
            raise HTTPException(status_code=500)
      
        except KeyError as k_err:
            loguru_app_logger.exception(err)
            raise HTTPException(status_code=500)
        
        return transcript
