from typing import Optional

from pydantic import BaseModel, HttpUrl


class ExternalIDs(BaseModel):
    itunes_id: Optional[str]
    spotify_id: Optional[str]
    podchaser_id: Optional[str]
    listennotes_id: Optional[str]

    def to_dict(self):
        return {
            "itunes_id": self.itunes_id,
            "spotify_id": self.spotify_id,
            "podchaser_id": self.podchaser_id,
            "listennotes_id": self.listennotes_id,
        }


class ExternalURLs(BaseModel):
    itunes_url: Optional[HttpUrl]
    spotify_url: Optional[HttpUrl]
    podchaser_url: Optional[HttpUrl]
    listennotes_url: Optional[HttpUrl]

    def to_dict(self) -> dict:
        return {
            "itunes_url": self.itunes_url,
            "spotify_url": self.spotify_url,
            "podchaser_url": self.podchaser_url,
            "listennotes_url": self.listennotes_url,
        }


class MediaAssets(BaseModel):
    image_url: Optional[HttpUrl]
    feed_url: Optional[HttpUrl]

    def to_dict(self) -> dict:
        return {"image_url": self.image_url, "feed_url": self.feed_url}
