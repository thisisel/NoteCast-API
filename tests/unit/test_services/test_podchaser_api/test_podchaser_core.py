from note_cast.services.podchaser_api.graphql.core import PodchaserCoreUtils

def test_execute_query():

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
    data : dict = PodchaserCoreUtils.execute_query(query)

    
    assert data.get("podcasts") is not None
    assert data["podcasts"].get("data") is not None
    assert data["podcasts"].get("paginatorInfo") is not None
    assert len(data["podcasts"].get("data")) != 0