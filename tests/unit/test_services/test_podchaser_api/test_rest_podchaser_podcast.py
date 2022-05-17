import pytest
from httpx import Response
from note_cast.log.custom_logging import loguru_app_logger
# from note_cast.services.podchaser_api.rest import PodchaserPodcast
from note_cast.services.podchaser_api import PodchaserPodcastRequests


def test_request_search_podcast_term():
    """
    GIVEN podcast title as term, start and count as pagination params
    WHEN sending request to podchaser rest api for search query
    THEN return at least 1 json result(s)
    """
    response: Response = PodchaserPodcastRequests._request_search_podcast_term(
        term="Hidden", start=0, count=25
    )

    assert response.status_code == 200

    response_content = response.json()
    loguru_app_logger.debug(response_content)

    assert len(response_content) <= 25
    assert response_content.get("entities", None) is not None


def test_request_get_single_podcast():
    """
    GIVEN podcast id
    WHEN sending request to podchaser rest api
    THEN return single podcast requested
    """
    response: Response = PodchaserPodcastRequests._request_get_single_podcast(p_id=687224)
    assert response.status_code == 200

    response_content = response.json()
    loguru_app_logger.debug(response_content)
    assert response_content.get("id") == 687224


d = {
    "p_id": 687224,
    "p_title": "BPLUS بی‌پلاس پادکست فارسی خلاصه کتاب",
    "image_url": "https:\/\/ssl-static.libsyn.com\/p\/assets\/7\/6\/e\/6\/76e6250f8ab5a580\/itunes-covers-01.jpg",
    "description": "خلاصه‌ی فارسی کتابهای غیرداستانی",
    "feed_url": "https:\/\/bplus.libsyn.com\/rss",
}

@pytest.mark.parametrize("test_id,expected", [(687224, d)])
def test_get_single_podcast(test_id, expected):
    from note_cast.schemas import BasePodcast

    result = PodchaserPodcastRequests.get_single_podcast(p_id=test_id)
    assert isinstance(result, BasePodcast)


    assert result.p_id == str(expected['p_id'])
    # assert result.p_title == expected['p_title']
    # assert result.image_url == expected['image_url']
    # assert result.feed_url == expected['feed_url']
