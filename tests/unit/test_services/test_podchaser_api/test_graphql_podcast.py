from note_cast.services.podchaser_api import PodchaserPodcastGQueries
from note_cast.schemas import BasePodcast, PaginatorInfo, BaseEpisode


def test_search_podcast_term():
    podcasts, page_info = PodchaserPodcastGQueries.search_podcast_term(term="hidden")

    assert isinstance(podcasts, list)
    assert isinstance(podcasts[0], BasePodcast)
    assert isinstance(page_info, PaginatorInfo)


def test_search_podcast_related_episodes():
    (
        podcast,
        related_episodes,
        paginator_info,
    ) = PodchaserPodcastGQueries.fetch_podcast_related_episodes(p_id="687224")

    assert isinstance(podcast, BasePodcast)
    assert isinstance(paginator_info, PaginatorInfo)
    assert isinstance(related_episodes, list)
    assert isinstance(related_episodes[0], BaseEpisode)

def test_fetch_single_podcast():
    podcast = PodchaserPodcastGQueries.fetch_single_podcast(p_id="687224")

    assert isinstance(podcast, BasePodcast)
    assert podcast.p_id == "687224"
    assert podcast.web_url is not None
    assert podcast.p_title is not None
    assert podcast.description is not None
    assert podcast.image_url is not None
    assert podcast.feed_url is not None
    assert podcast.external_urls.podchaser_url is not None