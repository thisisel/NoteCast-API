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


class PodchaserPodcastGQueries:
    @classmethod
    def search_podcast_term(cls, term: str, page: int = 0):
        query = """
                query {{
                    podcasts(
                        searchTerm: "{search_term}"
                        sort: {{ sortBy: RELEVANCE }}
                        first: 10
                        page: {page}
                        paginationType: PAGE
                    ) {{
                        paginatorInfo {{
                            currentPage
                            hasMorePages
                            total
                        }}
                        data {{
                            id
                            title
                            url
                            webUrl
                            description
                            imageUrl
                            rssUrl
                        }}
                    }}
                }}
                """.format(
            search_term=term, page=page
        )

        try:

            data = PodchaserCoreUtils.execute_query(query=query)

            podcasts_response = data["podcasts"]["data"]
            pagination_response = data["podcasts"]["paginatorInfo"]

            podcasts: List[BasePodcast] = [
                BasePodcast(
                    p_id=p.get("id"),
                    p_title=p.get("title"),
                    description=p.get("description"),
                    feed_url=p.get("rssUrl"),
                    image_url=p.get("imageUrl"),
                    external_urls=ExternalURLs(podchaser_url=p.get("url")),
                )
                for p in podcasts_response
            ]

            paginator_info = PodchaserCoreUtils.make_pagination_info(
                pagination_response=pagination_response
            )

            return podcasts, paginator_info

        # TODO raise http exception in endpoints, raise ApiException (?) in helper methods
        except (KeyError, PodchaserException) as errors_tuple:
            if isinstance(errors_tuple[0], KeyError):
                loguru_app_logger(errors_tuple[0])

            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def fetch_single_podcast(cls, p_id: str):
        query = """
                query {{
                    podcast(identifier: {{ id: "{p_id}", type: PODCHASER }}) {{
                        id
                        title
                        description
                        url
                        imageUrl
                        rssUrl
                        webUrl
                    }}
                }}
                """.format(
            p_id=p_id
        )

        try:
            data = PodchaserCoreUtils.execute_query(query=query)

            podcast_response = data["podcast"]

            podcast: BasePodcast = BasePodcast(
                p_id=podcast_response.get("id"),
                p_title=podcast_response.get("title"),
                web_url=podcast_response.get("webUrl"),
                description=podcast_response.get("description"),
                image_url=podcast_response.get("imageUrl"),
                feed_url=podcast_response.get("rssUrl"),
                external_urls=ExternalURLs(podchaser_url=podcast_response.get("url")),
            )
            return podcast

        except KeyError as k_err:
            loguru_app_logger.error(k_err)
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except PodchaserException:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def fetch_podcast_related_episodes(
        cls,
        p_id: str,
        episode_search_term: str = None,
        first: int = 10,
        page: int = 0,
        from_air_date: str = None,
        to_air_date: str = None,
    ):

        ep_search_term_slot = (
            f'searchTerm: "{episode_search_term}"' if episode_search_term else ''
        )
        from_slot = f'from: "{from_air_date}",' if from_air_date is not None else ''
        to_slot = f'to: "{to_air_date}"' if to_air_date is not None else ''
        air_date_slot = f'airDate: {{ {from_slot} {to_slot} }}'
        filters_slot = f'filters: {{ {air_date_slot} }}'

        query = """
            query {{
            podcast(identifier: {{ id: "{p_id}", type: PODCHASER }}) {{
                id
                title
                url
                webUrl

                episodes(
                        paginationType: PAGE
                        first: {first}
                        page: {page}
                        {episode_search_term}
                        {filters}
                    
                    
                    ) {{
                        paginatorInfo {{
                            currentPage
                            hasMorePages
                            total
                        }}
                        data {{
                            id
                            title
                            imageUrl
                            audioUrl
                            description
                            airDate
                        }}
                    }}
                }}
            }}
        
        """.format(
            p_id=p_id,
            episode_search_term=ep_search_term_slot,
            first=first,
            page=page,
            filters=filters_slot,
        )

        try:
            data = PodchaserCoreUtils.execute_query(query=query)

            podcast_response = data["podcast"]
            rel_episodes_response = podcast_response["episodes"]["data"]
            pagination_response = podcast_response["episodes"]["paginatorInfo"]

            podcast: BasePodcast = BasePodcast(
                p_id=podcast_response.get("id"),
                p_title=podcast_response.get("title"),
                web_url=podcast_response.get("webUrl"),
                external_urls=ExternalURLs(podchaser_url=podcast_response.get("url")),
            )

            related_episodes: List[BaseEpisode] = [
                BaseEpisode(
                    e_id=e.get("id"),
                    e_title=e.get("title"),
                    image_url=e.get("imageUrl"),
                    audio_url=e.get("audioUrl"),
                    description=e.get("description"),
                    air_date=e.get("airDate"),
                )
                for e in rel_episodes_response
            ]

            paginator_info = PodchaserCoreUtils.make_pagination_info(
                pagination_response=pagination_response
            )

            return podcast, related_episodes, paginator_info

        except KeyError as k_err:
            loguru_app_logger.error(k_err)
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except PodchaserException as p_exc:
            loguru_app_logger.error(p_exc)
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
