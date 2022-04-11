from ..models import Episode, Podcast


class EpisodeQuery:
    @staticmethod
    def find_episode(e_id: str = None, e_title: str = None):
        if e_id:
            return Episode.nodes.get_or_none(e_id=e_id)
        elif e_title:
            return Episode.nodes.get_or_none(title=e_title)
        raise TypeError(
            message="Invalid kwargs passed. Either p_id or title is accepted for podcast query"
        )

    @staticmethod
    def create_episode(e_id : str, e_title : str, audio_url : str, **kwargs):
        return Episode(e_id=e_id, e_title=e_title, audio_url=audio_url, **kwargs).save()

    @classmethod
    def get_source_podcast_or_none(cls, episode: Episode)-> Podcast:
        return episode.published_for.single()
