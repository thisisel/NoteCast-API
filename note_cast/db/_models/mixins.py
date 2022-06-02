from neomodel import (
    StringProperty,
)


class ExternalIDsMixin(object):
    itunes_id = StringProperty(index=True)
    spotify_id = StringProperty(index=True)
    podchaser_id = StringProperty(index=True)
    listennotes_id = StringProperty(index=True)

    def to_dict(self):
        return {
            "itunes_id": self.itunes_id,
            "spotify_id": self.spotify_id,
            "podchaser_id": self.podchaser_id,
            "listennotes_id": self.listennotes_id,
        }


class ExternalURLsMixin(object):
    itunes_url = StringProperty()
    spotify_url = StringProperty()
    podchaser_url = StringProperty()
    listennotes_url = StringProperty()

    def to_dict(self) -> dict:
        return {
            "itunes_url": self.itunes_url,
            "spotify_url": self.spotify_url,
            "podchaser_url": self.podchaser_url,
            "listennotes_url": self.listennotes_url,
        }


class MediaAssetsMixin(object):
    image_url = StringProperty()
    feed_url = StringProperty()

    def to_dict(self) -> dict:
        return {"image_url": self.image_url, "feed_url": self.feed_url}
