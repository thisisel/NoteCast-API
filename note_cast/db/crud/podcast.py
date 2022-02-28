from ..models import Podcast, Episode
from neomodel import db


class PodcastQuery:
    @staticmethod
    def get_podcast(p_id: str = None, p_title: str = None):
        if p_id:
            return Podcast.nodes.get_or_none(p_id=p_id)
        elif p_title:
            return Podcast.nodes.get_or_none(p_title=p_title)
        raise TypeError(
            message="Invalid kwargs passed. Either p_id or title is accepted for podcast query"
        )

    @staticmethod
    def create_podcast(p_id: str, p_title: str, p_listennotes_url: str, **kwargs):
        return Podcast(
            p_id=p_id, p_title=p_title, p_listennotes_url=p_listennotes_url
        ).save()

    @staticmethod
    def get_related_episode(podcast: Podcast, e_id: str):
        rows, cols = db.cypher_query(
            "MATCH (p:Podcast)-[rel:PUBLISHED_FOR]-(e:Episode) "
            "WHERE p.p_id = $p_id AND e.e_id = $e_id RETURN DISTINCT (e)",
            params={"p_id": podcast.p_id, "e_id": e_id},
        )

        return Episode.inflate(rows[0][0]) if len(rows) != 0 else None
