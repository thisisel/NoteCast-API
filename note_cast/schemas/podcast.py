import typing
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from .notes import Note


class EpisodeTimestamp(BaseModel):
    hour: int
    minute: int
    seconds: int


class Quote(BaseModel):
    q_id: str
    transcript: typing.Optional[str]
    visible: bool = True
    attachments: typing.List[Note]


class QuoteMetadata(BaseModel):
    audio_url: str

    start_timestamp: EpisodeTimestamp
    end_timestamp: EpisodeTimestamp

    p_id: str
    e_id: str

    p_title: str = None
    e_title: str = None

    p_listennotes_url: HttpUrl = None
    e_listennotes_url: HttpUrl = None

    new_podcast: bool = False
    new_episode: bool = False


class Episode(BaseModel):
    e_id: int
    e_title: str
    published_on: datetime
    e_listennotes_url: HttpUrl
    audio_url: HttpUrl
    length_h: int
    length_m: int
    length_s: int
    quotes: typing.List["Quote"]


class Podcast(BaseModel):
    p_id: str
    title: str
    listennotes_url: HttpUrl
    category: str  # TODO enum
    episodes: typing.List[Episode]
