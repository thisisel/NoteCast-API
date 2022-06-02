from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, HttpUrl, validator, Field

from .mixins import ExternalIDs, ExternalURLs
from .podcast import BasePodcast


class BaseEpisode(BaseModel):

    e_id: int
    e_title: str
    air_date: Optional[datetime] = None
    image_url: Optional[Union[HttpUrl, str]] = Field(
        default=None,
        description="this field either has a value or if not None by default,is of length zero ",
    )
    audio_url: Optional[HttpUrl] = None
    length_s: Optional[int] = None
    description: Optional[str] = None
    podcast: Optional[BasePodcast]
    external_ids: Optional[ExternalIDs] = None
    external_urls: Optional[ExternalURLs] = None

    @validator("image_url")
    def image_url_is_empty(cls, v):
        if len(v) == 0:
            return ""
        elif isinstance(v, HttpUrl):
            return v
        else:
            raise ValueError(f'image_url = "{v}" does not comply with Http Url')
