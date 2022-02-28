from ..models import Episode


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
    def create_episode(e_id : str, e_title : str, e_listennotes_url : str, audio_url : str, **kwargs):
        return Episode(e_id=e_id, e_title=e_title, e_listennotes_url=e_listennotes_url, audio_url=audio_url).save()
