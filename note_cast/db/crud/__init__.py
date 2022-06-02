#TODO move all queries to models
#TODO separate models into modules

from .podcast import PodcastQuery, Podcast as PodcastNode
from .episode import EpisodeQuery, Episode as EpisodeNode
from .quote import QuoteQuery, Quote as QuoteNode
from .note import NoteQuery, Note as NoteNode
from .user import UserQuery, User, load_user
