from typing import List, Union

from fastapi import status
from httpx import Response
from httpx._exceptions import HTTPStatusError
from note_cast.api.errors import CustomHTTPException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import BasePodcast
from .. import base_url, headers, httpx_client_factory


class PodchaserPodcast:
    @classmethod
    def _request_search_podcast_term(cls, term: str, start: int, count: int):

        client = httpx_client_factory(base_url=base_url, headers=headers)

        try:
            with client:

                url = "list/podcast"
                payload = {
                    "start": start,
                    "count": count,
                    "sort_order": "SORT_ORDER_RELEVANCE",
                    "sort_direction": "desc",
                    "filters": {"term": term},
                    "options": {},
                }

                response: Response = client.post(url=url, json=payload)

            return response

        except HTTPStatusError as exc:
            loguru_app_logger.exception(exc)

    @classmethod
    def search_podcast_term(cls, term: str, start: int = 0, count: int = 25):
        

        response: Union[Response, None] = cls._request_search_podcast_term(
            term=term, start=start, count=count
        )

        if response is None:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        json_content = response.json()

        try:
            if (_ := json_content["total"]) == 0:
                raise CustomHTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"search query for {term} returned 0 result",
                )

            entities: List[dict] = json_content["entities"]
            search_results: List[BasePodcast] = [
                BasePodcast(
                    p_id=entity["id"],
                    p_title=entity["title"],
                    image_url=entity["image_url"],
                    description=entity["description"],
                    feed_url=entity["feed_url"]
                )
                for entity in entities
            ]
       
        except KeyError as k_err:
            loguru_app_logger.error(k_err)
        
        return search_results

    @classmethod
    def _request_get_single_podcast(cls, p_id: int):

        client = httpx_client_factory(base_url=base_url, headers=headers)

        try:
            with client:

                url = f"podcasts/{p_id}/"

                response: Response = client.get(url=url)

            return response

        except HTTPStatusError as exc:
            loguru_app_logger.exception(exc)
            if exc.response.status_code == 404:
                return exc.response

    @classmethod
    def get_single_podcast(cls, p_id: int):

        response: Union[Response, None] = cls._request_get_single_podcast(p_id=p_id)

        if response is None:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if response.status_code == 404:
            raise CustomHTTPException(status_code=status.HTTP_404_NOT_FOUND)


        json_content = response.json()

        get_result: BasePodcast = BasePodcast(
                p_id=json_content["id"],
                p_title=json_content["title"],
                image_url=json_content["image_url"],
                description=json_content["description"],
                feed_url=json_content["feed_url"]
            )
    

        return get_result
