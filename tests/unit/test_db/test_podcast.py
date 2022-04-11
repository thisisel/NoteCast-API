from note_cast.db.crud import PodcastQuery
import logging

def test_find_podcast_quotes():
    result = PodcastQuery.get_podcast_quotes(p_id=57847)

    assert len(result) == 1

    p = result[0]
    # assert p.q_id == '59e1591cfd3a14ea'
    logging.debug(result)
