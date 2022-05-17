from typing import List
from fastapi import status
from note_cast.api.errors import CustomHTTPException
from note_cast.api.errors.podchaser_exception import PodchaserException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import (
    BasePodcast,
    ExternalURLs,
    BaseEpisode,
)
from .core import PodchaserCoreUtils


class PodchaserEpisodeGQueries:
    @classmethod
    def search_episode(cls, term: str, page: int = 0):
        query = """
                query {{
                    episodes (
                        searchTerm: "{search_term}" 
                        sort: {{sortBy:RELEVANCE}}
                        first:10, page:{page}
                        paginationType:PAGE
                    ) {{
                        paginatorInfo {{
                            currentPage
                            hasMorePages
                            total
                        }}
                        data {{
                            id
                            title
                            audioUrl
                            fileSize
                            imageUrl
                            length
                            description
                            airDate
                            podcast {{
                                id
                                title
                                
                            }}
                        }}
                    }}
                }}
                """.format(
            search_term=term, page=page
        )

        try:
            data = PodchaserCoreUtils.execute_query(query=query)

            episodes_response = data["episodes"]["data"]
            pagination_response = data["episodes"]["paginatorInfo"]

            episodes: List[BaseEpisode] = [
                BaseEpisode(
                    e_id=e.get("id"),
                    e_title=e.get("title"),
                    audio_url=e.get("audioUrl"),
                    image_url=e.get("imageUrl"),
                    length_s=e.get("length"),
                    description=e.get("description"),
                    air_date=e.get("airDate"),
                    podcast=BasePodcast(
                        p_id=e.get("podcast").get("id"),
                        p_title=e.get("podcast").get("title"),
                    ),
                )
                for e in episodes_response
            ]

            paginator_info = PodchaserCoreUtils.make_pagination_info(
                pagination_response=pagination_response
            )

            return episodes, paginator_info

        except KeyError as k_err:
            loguru_app_logger.error(k_err)
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except PodchaserException:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def fetch_single_episode(cls, e_id: str):
        query = """
                    query {{
                        episode(identifier: {{ id: "{e_id}", type: PODCHASER }}) {{
                            id
                            title
                            description
                            url
                            imageUrl
                            airDate
                            audioUrl
                            length
                            podcast{{
                                id
                                title
                                url
                                webUrl
                            }}
                        }}
                    }}
                """.format(
            e_id=e_id
        )

        try:
            data = PodchaserCoreUtils.execute_query(query=query)
            episode_response = data["episode"]

            episode: BaseEpisode = BaseEpisode(
                e_id=episode_response.get("id"),
                e_title=episode_response.get("title"),
                description=episode_response.get("description"),
                image_url=episode_response.get("imageUrl"),
                air_date=episode_response.get("airDate"),
                audio_url=episode_response.get("audioUrl"),
                length_s=episode_response.get("length"),
                external_urls=ExternalURLs(podchaser_url=episode_response.get("url")),
            )

            return episode

        except KeyError as k_err:
            loguru_app_logger.error(k_err)
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except PodchaserException:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
