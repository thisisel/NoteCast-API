from note_cast.db.crud import PodcastQuery , PodcastNode, EpisodeNode

def test_create_podcast():
    pass


def test_read_podcast():
    pass

def test_update_podcast():
    pass

def test_delete_podcast():
    pass

def test_get_related_quotes():
    e : EpisodeNode = EpisodeNode.nodes.get(e_id='2515594')
    assert e.e_id == '2515594'

    q_list = e.quotes_list
    print(q_list)

