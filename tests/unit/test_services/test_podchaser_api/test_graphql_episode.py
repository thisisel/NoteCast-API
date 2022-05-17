from note_cast.services.podchaser_api import PodchaserEpisodeGQueries
from note_cast.schemas import BaseEpisode, PaginatorInfo


def test_search_episode():
    episodes, paginator_info = PodchaserEpisodeGQueries.search_episode("bplus")

    assert isinstance(episodes, list)
    assert isinstance(episodes[0], BaseEpisode)
    assert isinstance(paginator_info, PaginatorInfo)


def test_fetch_single_episode():
    episode = PodchaserEpisodeGQueries.fetch_single_episode("32406606")
    assert isinstance(episode, BaseEpisode)
