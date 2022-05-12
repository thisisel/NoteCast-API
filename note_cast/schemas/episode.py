from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, HttpUrl

from .mixins import ExternalIDs, ExternalURLs
from .podcast import BasePodcast


class BaseEpisode(BaseModel):
    e_id: int
    e_title: str
    image_url: Optional[HttpUrl] = None
    audio_url: Optional[HttpUrl] = None
    length_s: Optional[int] = None
    description: Optional[str] = None
    podcast: Optional[BasePodcast]
    external_ids: Optional[ExternalIDs] = None
    external_urls: Optional[ExternalURLs] = None
