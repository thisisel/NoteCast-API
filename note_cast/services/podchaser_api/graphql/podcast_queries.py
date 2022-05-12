from typing import List
from fastapi import status
from note_cast.api.errors import CustomHTTPException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import BasePodcast, ExternalURLs
from .. import gq_client as client


class PodchaserPodcastGQueries:
    @classmethod
    def _execute_query(cls, query: str):
        response = client.execute(query=query)
        if (errors := response.get("errors", None)) is not None:
            loguru_app_logger.error(errors)
            return

        try:
            data = response["data"]
            return data

        except KeyError as k_err:
            loguru_app_logger.exception(k_err)

    @classmethod
    def search_podcast_term(cls, term: str):
        query = """
                query {{
                    podcasts(
                        searchTerm: {search_term}
                        sort: {{ sortBy: RELEVANCE }}
                        first: 10
                        page: 0
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
            search_term=term
        )

        if (data := cls._execute_query(query=query)) is not None:
           
            if (podcasts_response := data.get("podcasts")) is not None:

                
                
                podcasts : List[BasePodcast] = [
                    BasePodcast(
                        p_id=p.get("id"),
                        p_title=p.get("title"),
                        description=p.get("description"),
                        feed_url=p.get("rssUrl"),
                        image_url=p.get("imageUrl"),
                        external_urls=ExternalURLs(podchaser_url=p.get("url"))
                    )
                    for p in podcasts_response
                ]


                # podcasts : List[BasePodcast] = []
                # for p in podcasts_response:
                #     ext_urls = ExternalURLs(podchaser_url=p.get("url"))
                #     BasePodcast(
                #         p_id=p.get("id"),
                #         p_title=p.get("title"),
                #         description=p.get("description"),
                #         feed_url=p.get("rssUrl"),
                #         image_url=p.get("imageUrl"),
                #         external_urls=ext_urls
                #     )
                #     podcasts.append(BasePodcast)
                
                return podcasts

        else:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def search_podcast_related_episodes(cls, p_id: str):
        query = """
            query {{
            podcast(identifier: {{ id: "{p_id}", type: PODCHASER }}) {{
                id
                title
                url
                webUrl

                episodes(paginationType: PAGE, first: 10, page: 0) {{
                        paginatorInfo {{
                            currentPage
                            hasMorePages
                            total
                        }}
                        data {{
                            id
                            title
                            imageUrl
                            description
                            airDate
                        }}
                    }}
                }}
            }}
        
        """.format(
            p_id=p_id
        )

        if (data := cls._execute_query(query=query)) is not None:
            return data
        else:
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
