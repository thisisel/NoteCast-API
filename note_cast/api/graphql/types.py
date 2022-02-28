import typing
from datetime import datetime

import strawberry

from .interfaces import IGQResponse, IUser


@strawberry.type
class GQApiResponse(IGQResponse):
    ...


@strawberry.type
class GQApiErrorResponse(IGQResponse):
    category: typing.Optional[str]
    status : bool


@strawberry.type
class UserDB(IUser):
    u_id: strawberry.ID
    username: str
    email: str
    password_hash: str


@strawberry.type
class User(IUser):
    u_id: strawberry.ID
    username: str
    email: str


@strawberry.type
class Podcast:
    p_id: str
    p_title: str
    category: str  # TODO enum
    p_listennotes_url : str
    episodes: typing.List["Episode"]


@strawberry.type
class Episode:
    e_id: int
    e_title: str
    published_on: datetime
    audio_url: str
    e_listennotes_url : str
    length_h: int
    length_m: int
    length_s: int
    quotes: typing.List["Quote"]


@strawberry.type
class Quote:
    q_id: int
    transcript: str
    start_time_h: int
    start_time_m: int
    start_time_s: int
    end_time_h: int
    end_time_m: int
    end_time_s: int
    episode: "Episode"
    podcast: "Podcast"
    notes: typing.List["Note"]
    # bookmark by users


@strawberry.type
class Note:
    n_id: int
    text: str
    author: "IUser"
    comments: typing.List["Comment"]
    # star by original author
    # like by users


@strawberry.type
class Comment:
    id: int
    text: str
