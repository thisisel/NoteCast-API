from __future__ import annotations
from typing import TYPE_CHECKING, Union, List

from neomodel import (
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    Q
)

from .mixins import ExternalIDsMixin, MediaAssetsMixin

if TYPE_CHECKING:
    from .quote import Quote


class Podcast(StructuredNode, ExternalIDsMixin, MediaAssetsMixin):
    p_id = StringProperty(required=True, index=True)
    p_title = StringProperty(required=True, index=True)
    description = StringProperty()
    web_url = StringProperty()

    category = RelationshipTo(".category.Category", "CATEGORIZED_UNDER")
    episodes = RelationshipFrom(".episode.Episode", "PUBLISHED_FOR")

    @classmethod
    def get_podcast(p_id: str = None, p_title: str = None)->Union[Podcast, None]:
        if p_id:
            return Podcast.nodes.get_or_none(p_id=p_id)
        elif p_title:
            return Podcast.nodes.get_or_none(p_title=p_title)
        raise TypeError(
            message="Invalid kwargs passed. Either p_id or title is accepted for podcast query"
        )

    @classmethod
    def search_podcasts(cls, p_id: str = None, p_title=None) -> List[Podcast]:

        kwargs = {"p_id": p_id, "p_title": p_title}
        query_filters = {"p_id": Q(p_id=p_id), "p_title": Q(p_title__contains=p_title)}
        query_filters_masked = [
            query_filters.get(filter)
            for filter, argument in kwargs.items()
            if argument is not None
        ]

        podcasts = Podcast.nodes.filter(*query_filters_masked).all()
        # podcasts = Podcast.nodes.filter(Q(p_title__contains=p_title)).all()
        return podcasts

    # TODO filter on air date
    def episodes_list(self, **kwargs):
        skip = kwargs.get("skip")
        limit = kwargs.get("limit")
        e_list = [e for e in self.episodes][skip:limit]
        return e_list

    def quotes_list(self, skip: int = 0, limit: int = 20, to_dict: bool = False):

        rows, cols = self.cypher(
            "MATCH (q:Quote)-[:MENTIONED_ON]-(e:Episode)-[:PUBLISHED_FOR]-(p:Podcast) WHERE p.p_id=$p_id RETURN q ORDER BY id(q) SKIP $skip LIMIT $limit",
            params={"p_id": self.p_id, "skip": skip, "limit": limit},
        )
        return [
            Quote.inflate(r[0]) if not to_dict else Quote.inflate(r[0]).to_dict()
            for r in rows
        ]

    def to_dict(self, include_episodes: bool = False) -> dict:
        result: dict = {
            "p_id": self.p_id,
            "p_title": self.p_title,
            "description": self.description,
            "web_url": self.web_url,
            "itunes_id": self.itunes_id,
            "spotify_id": self.spotify_id,
            "podchaser_id": self.podchaser_id,
        }
        if include_episodes:
            e_db_list = self.episodes_list()
            e_list = [e_db.to_dict() for e_db in e_db_list]
            result.update({"episodes": e_list})

        return result
