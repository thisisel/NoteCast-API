from python_graphql_client import GraphqlClient
from note_cast.log.custom_logging import loguru_app_logger
from .. import headers


class PodchaserPodcastQueries:
    @classmethod
    def search_podcast(cls, term: str):
        query = """
                query {
                    podcasts(
                        searchTerm: {search_term}
                        sort: { sortBy: RELEVANCE }
                        first: 10
                        page: 0
                        paginationType: PAGE
                    ) {
                        paginatorInfo {
                            currentPage
                            hasMorePages
                            total
                        }
                        data {
                            id
                            title
                            description
                            url
                            imageUrl
                            rssUrl
                            webUrl
                        }
                    }
                }
                """.format(search_term=term)
        
        response = GraphqlClient.execute(query=query, headers=headers)
        if (errors := response.get('errors', None)) is not None:
            loguru_app_logger.error(errors)
            return
        
        try:
            data = response['data']

        except KeyError as k_err:
            loguru_app_logger.exception(k_err)
