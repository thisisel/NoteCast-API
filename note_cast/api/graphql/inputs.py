import strawberry
from pydantic import HttpUrl


@strawberry.input
class EpisodeTimestamp:
    hour: int
    minute: int
    seconds: int


@strawberry.input
class QuoteMetadata:
    audio_url: str

    start_timestamp: EpisodeTimestamp
    end_timestamp: EpisodeTimestamp

    p_id: str
    e_id: str
    p_title: str = None
    e_title: str = None

    new_podcast: bool = False
    new_episode: bool = False