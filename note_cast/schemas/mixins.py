from typing import Optional

from pydantic import BaseModel, HttpUrl


class ExternalIDs(BaseModel):
    itunes_id: Optional[str]
    spotify_id: Optional[str]
    podchaser_id: Optional[str]
    listennotes_id: Optional[str]


class ExternalURLs(BaseModel):
    itunes_url: Optional[HttpUrl] = None
    spotify_url: Optional[HttpUrl] = None
    podchaser_url: Optional[HttpUrl] = None
    listennotes_url: Optional[HttpUrl] = None


class MediaAssets(BaseModel):
    image_url: Optional[HttpUrl] = None
    feed_url: Optional[HttpUrl] = None
