from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, HttpUrl

from .mixins import ExternalIDs, ExternalURLs
from .podcast import BasePodcast


class BaseEpisode(BaseModel):
    e_id: int
    e_title: str
    image_url: Optional[HttpUrl]
    audio_url: Optional[HttpUrl]
    length_s: Optional[int]
    description: Optional[str]
    podcast: Optional[BasePodcast]
    external_ids: Optional[ExternalIDs]
    external_urls: Optional[ExternalURLs]
