from typing import List
from ..models import Episode, Podcast, Quote


class EpisodeQuery:
    @classmethod
    def find_episode(cls, e_id: str = None, e_title: str = None):
        if e_id:
            return Episode.nodes.get_or_none(e_id=e_id)
        elif e_title:
            return Episode.nodes.get_or_none(title=e_title)
        raise TypeError(
            message="Invalid kwargs passed. Either p_id or title is accepted for podcast query"
        )

    #TODO DEPRECATE
    @classmethod
    def create_episode(cls, e_id : str, e_title : str, audio_url : str, **kwargs):
        return Episode(e_id=e_id, e_title=e_title, audio_url=audio_url, **kwargs).save()

    #TODO DEPRECATE
    @classmethod
    def get_source_podcast_or_none(cls, episode: Episode)-> Podcast:
        return episode.published_for.single()
    
    #TODO DEPRECATE
    @classmethod
    def get_related_quotes(cls, e_id : str):
        if (e := cls.find_episode(e_id=e_id)) is not None:
            return e.quotes_list()
