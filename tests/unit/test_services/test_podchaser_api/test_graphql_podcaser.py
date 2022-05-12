import pytest
from httpx import Response
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.services.podchaser_api.graphql import PodchaserPodcastGQueries
from note_cast.schemas import BasePodcast

podcasts_term : str = "bpuls"

def test_execute_search_podcast_term():
    query = """
            query {{
                podcasts(
                    searchTerm: "{search_term}"
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
                        description
                        url
                        imageUrl
                        rssUrl
                        webUrl
                    }}
                }}
            }}
            """.format(
                    search_term="hidden"
                    )
    data : dict = PodchaserPodcastGQueries._execute_query(query)

    
    assert data.get("podcasts") is not None
    assert data["podcasts"].get("data") is not None
    assert data["podcasts"].get("paginatorInfo") is not None
    assert len(data["podcasts"].get("data")) != 0


def test_search_podcast_term():
    podcasts = PodchaserPodcastGQueries.search_podcast_term(term=podcasts_term)
    
    assert isinstance(podcasts, list)
    assert isinstance(podcasts[0], BasePodcast)