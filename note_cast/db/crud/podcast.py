from typing import List

from neomodel import Q, db

from ..models import Episode, Podcast


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

    @staticmethod
    def create_podcast(p_id: str, p_title: str, **kwargs):
        return Podcast(p_id=p_id, p_title=p_title, **kwargs).save()

    @staticmethod
    def get_related_episode(podcast: Podcast, e_id: str):
        rows, cols = db.cypher_query(
            "MATCH (p:Podcast)-[rel:PUBLISHED_FOR]-(e:Episode) "
            "WHERE p.p_id = $p_id AND e.e_id = $e_id RETURN DISTINCT (e)",
            params={"p_id": podcast.p_id, "e_id": e_id},
        )

        return Episode.inflate(rows[0][0]) if len(rows) != 0 else None

    @classmethod
    def get_podcast_quotes(cls, p_id: str):
        if(podcast := Podcast.nodes.get_or_none(p_id=p_id)) is not None:
            episodes = podcast.episodes.all()
            quotes = [episode.quotes.all() for episode in episodes]
            return quotes