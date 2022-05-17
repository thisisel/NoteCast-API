from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, validator

from .mixins import ExternalIDs, ExternalURLs
from .podcast import BasePodcast


class BaseEpisode(BaseModel):
    e_id: int
    e_title: str
    air_date : Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    audio_url: Optional[HttpUrl] = None
    length_s: Optional[int] = None
    description: Optional[str] = None
    podcast: Optional[BasePodcast]
    external_ids: Optional[ExternalIDs] = None
    external_urls: Optional[ExternalURLs] = None


    @validator('image_url')
    def image_url_is_empty(cls, v):
        if len(v) == 0:
            return None
