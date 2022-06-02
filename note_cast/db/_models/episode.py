from __future__ import annotations
from typing import TYPE_CHECKING


from neomodel import (
    IntegerProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
)

from .mixins import ExternalIDsMixin, MediaAssetsMixin
from .relationships import PublishRel, MentionRel

if TYPE_CHECKING:
    from .podcast import Podcast


class Episode(StructuredNode, ExternalIDsMixin, MediaAssetsMixin):
    e_id = StringProperty(required=True, index=True)
    e_title = StringProperty(required=True, index=True)
    audio_url = StringProperty(required=True)
    length_s = IntegerProperty()
    num = IntegerProperty()
    description = StringProperty()

    published_for = RelationshipTo(
        ".podcast.Podcast", "PUBLISHED_FOR", model=PublishRel
    )
    quotes = RelationshipFrom(".quote.Quote", "MENTIONED_ON", model=MentionRel)

    @property
    def podcast(self) -> Podcast:
        return self.published_for.single()

    @property
    def air_date(self) -> PublishRel:
        if self.podcast:
            return self.published_for.relationship(self.podcast)

    @classmethod
    def find_episode(cls, e_id: str = None, e_title: str = None):
        if e_id:
            return Episode.nodes.get_or_none(e_id=e_id)
        elif e_title:
            return Episode.nodes.get_or_none(title=e_title)
        raise TypeError(
            message="Invalid kwargs passed. Either p_id or title is accepted for podcast query"
        )

    def quotes_list(self, to_dict: bool = False, **kwargs):
        skip = kwargs.get("skip")
        limit = kwargs.get("limit")
        q_list = [q if not to_dict else q.to_dict() for q in self.quotes][skip:limit]
        return q_list

    def to_dict(
        self, include_podcast: bool = False, include_quotes: bool = False
    ) -> dict:
        result = {
            "e_id": self.e_id,
            "e_title": self.e_title,
            "audio_url": self.audio_url,
            "length_s": self.length_s,
            "num": self.num,
            "description": self.description,
        }
        if include_podcast:
            result.update({"podcast": self.podcast.to_dict()})
        if include_quotes:
            q_db_list = self.quotes_list
            q_list = [q_db.to_dict() for q_db in q_db_list]
            result.update({"quotes": q_list})

        return result
