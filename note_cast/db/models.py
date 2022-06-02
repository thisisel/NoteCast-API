from datetime import datetime
from typing import List, Union
from neomodel import (
    BooleanProperty,
    DateTimeProperty,
    EmailProperty,
    IntegerProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    ZeroOrMore,
)
from note_cast.utils import PasswordManager
from note_cast.log.custom_logging import loguru_app_logger


class PublishRel(StructuredRel):
    air_date_db = DateTimeProperty(default_now=True)

    @property
    def air_date(self):
        return self.air_date_db

    @air_date.setter
    def air_date(self, a_date: Union[str, datetime]):
        try:
            self.air_date_db = (
                datetime.strptime(a_date, "%Y-%m-%d %H:%M:%S")
                if type(a_date) is str
                else a_date
            )
        except ValueError:
            loguru_app_logger.error(
                f"While inserting PublishRel , {a_date} format does not match with pattern"
            )
            raise ValueError


class MentionRel(StructuredRel):
    start_offset_h = IntegerProperty(required=True)
    start_offset_m = IntegerProperty(required=True)
    start_offset_s = IntegerProperty(required=True)
    end_offset_h = IntegerProperty(required=True)
    end_offset_m = IntegerProperty(required=True)
    end_offset_s = IntegerProperty(required=True)

    def to_dict(self) -> dict:
        return {
            "start_offset_h": self.start_offset_h,
            "start_offset_m": self.start_offset_m,
            "start_offset_s": self.start_offset_s,
            "end_offset_h": self.end_offset_h,
            "end_offset_m": self.end_offset_m,
            "end_offset_s": self.end_offset_s,
        }


class BaseNoteActionRel(StructuredRel):
    date = DateTimeProperty(default_now=True)


class LikeRel(BaseNoteActionRel):
    pass


class SaveRel(BaseNoteActionRel):
    pass


class CommentRel(BaseNoteActionRel):
    pass


class ReplyRel(BaseNoteActionRel):
    pass


class AnnotateRel(BaseNoteActionRel):
    date_created = DateTimeProperty(default_now=True)
    ...


class Category(StructuredNode):
    name = StringProperty(required=True, unique_index=True)

    podcasts = RelationshipFrom("Podcast", "CATEGORIZED_UNDER")


class ExternalIDsMixin(object):
    itunes_id = StringProperty(index=True)
    spotify_id = StringProperty(index=True)
    podchaser_id = StringProperty(index=True)
    listennotes_id = StringProperty(index=True)

    def to_dict(self):
        return {
            "itunes_id": self.itunes_id,
            "spotify_id": self.spotify_id,
            "podchaser_id": self.podchaser_id,
            "listennotes_id": self.listennotes_id,
        }


class ExternalURLsMixin(object):
    itunes_url = StringProperty()
    spotify_url = StringProperty()
    podchaser_url = StringProperty()
    listennotes_url = StringProperty()

    def to_dict(self) -> dict:
        return {
            "itunes_url": self.itunes_url,
            "spotify_url": self.spotify_url,
            "podchaser_url": self.podchaser_url,
            "listennotes_url": self.listennotes_url,
        }


class MediaAssetsMixin(object):
    image_url = StringProperty()
    feed_url = StringProperty()

    def to_dict(self) -> dict:
        return {"image_url": self.image_url, "feed_url": self.feed_url}


class User(StructuredNode):
    u_id = UniqueIdProperty()
    username = StringProperty(unique=True, required=True)
    email: object = EmailProperty(required=True, unique_index=True)
    password_hash = StringProperty(required=True)
    disabled = BooleanProperty(default=False)
    joined_date_db = DateTimeProperty(default_now=True)

    notes = RelationshipTo(
        "Note", "ANNOTATED", model=AnnotateRel, cardinality=ZeroOrMore
    )
    bookmarks = RelationshipTo("Quote", "BOOKMARKED", cardinality=ZeroOrMore)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, plain_password):
        self.password_hash = PasswordManager.generate_password_hash(plain_password)

    def verify_password(self, plain_password):
        return PasswordManager.check_password_hash(plain_password, self.password_hash)

    @property
    def joined_date(self):
        return self.joined_date_db

    @joined_date.setter
    def joined_date(self, j_date: Union[str, datetime]):

        try:

            self.joined_date_db = (
                datetime.strptime(j_date, "%Y-%m-%d %H:%M:%S")
                if type(j_date) is str
                else j_date
            )
        except ValueError:
            loguru_app_logger.exception(
                f"While converting joined date , {j_date} format does not match with pattern"
            )
            raise ValueError

    def notes_list(self, **kwargs):
        skip = kwargs.get("skip")
        limit = kwargs.get("limit")
        n_list = [n for n in self.notes][skip:limit]
        return n_list

    def bookmarks_list(self, **kwargs):
        skip = kwargs.get("skip")
        limit = kwargs.get("limit")
        bk_list = [bk for bk in self.bookmarks][skip:limit]
        return bk_list

    def to_dict(self) -> dict:
        return {
            "u_id": self.u_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "disabled": self.disabled,
            "joined_date": self.joined_date,
        }


class Podcast(StructuredNode, ExternalIDsMixin, MediaAssetsMixin):
    p_id = StringProperty(required=True, index=True)
    p_title = StringProperty(required=True, index=True)
    description = StringProperty()
    web_url = StringProperty()

    category = RelationshipTo(Category, "CATEGORIZED_UNDER")
    episodes = RelationshipFrom("Episode", "PUBLISHED_FOR")

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


class Episode(StructuredNode, ExternalIDsMixin, MediaAssetsMixin):
    e_id = StringProperty(required=True, index=True)
    e_title = StringProperty(required=True, index=True)
    audio_url = StringProperty(required=True)
    length_s = IntegerProperty()
    num = IntegerProperty()
    description = StringProperty()

    published_for = RelationshipTo("Podcast", "PUBLISHED_FOR", model=PublishRel)
    quotes = RelationshipFrom("Quote", "MENTIONED_ON", model=MentionRel)

    @property
    def podcast(self) -> Podcast:
        return self.published_for.single()

    @property
    def air_date(self) -> PublishRel:
        if self.podcast:
            return self.published_for.relationship(self.podcast)

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


class Quote(StructuredNode):
    q_id = StringProperty(required=True, unique_index=True)
    transcript = StringProperty()
    visible = BooleanProperty(default=True)

    mentioned_on = RelationshipTo("Episode", "MENTIONED_ON", model=MentionRel)
    attachments = RelationshipFrom("Note", "ATTACHED_TO")
    bookmarked_by = RelationshipFrom("User", "BOOKMARKED", cardinality=ZeroOrMore)

    @property
    def episode(self) -> Episode:
        return self.mentioned_on.single()

    @property
    def mention_time(self) -> MentionRel:
        return self.mentioned_on.relationship(self.episode)

    def bookmarkers_list(self, **kwargs):
        skip = kwargs.get("skip")
        limit = kwargs.get("limit")
        bk_list = [q for q in self.bookmarked_by][skip:limit]
        return bk_list

    def to_dict(
        self, include_episode: bool = False, include_podcast: bool = False
    ) -> dict:
        result: dict = {
            "q_id": self.q_id,
            "transcript": self.transcript,
            "visible": self.visible,
            "mention_time": self.mention_time.to_dict(),
        }
        if include_episode:
            result.update({"episode": self.episode.to_dict(include_podcast)})
        return result


class Note(StructuredNode):
    n_id = UniqueIdProperty()
    text = StringProperty(required=True)
    is_public = BooleanProperty(default=False)

    author = RelationshipFrom("User", "ANNOTATED", model=AnnotateRel, cardinality=One)
    attach_to = RelationshipTo("Quote", "ATTACHED_TO")

    @property
    def writer(self) -> User:
        """return author single node"""
        return self.author.single()

    @property
    def quote(self) -> Quote:
        return self.attach_to.single()

    def to_dict(
        self,
        include_author: bool = False,
        include_quote: bool = False,
        include_episode: bool = False,
        include_podcast: bool = False,
    ) -> dict:
        result = {
            "n_id": self.n_id,
            "text": self.text,
            "is_public": self.is_public,
        }
        if include_author:
            result.update({"author": self.writer.to_dict()})
        if include_quote:
            result.update(
                {"quote": self.quote.to_dict(include_episode, include_podcast)}
            )

        return result
