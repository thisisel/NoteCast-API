from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, HttpUrl

from .mixins import ExternalIDs, ExternalURLs


# TODO add external IDs as mixin to pydantic
class BasePodcast(BaseModel):
    p_id: str
    p_title: str
    image_url: Optional[HttpUrl] = None
    feed_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    external_ids: Optional[ExternalIDs]
    external_urls: Optional[ExternalURLs]
