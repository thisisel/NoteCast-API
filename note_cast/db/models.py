from neomodel import (BooleanProperty, DateTimeProperty, EmailProperty,
                      IntegerProperty, One, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, StructuredRel,
                      UniqueIdProperty, ZeroOrMore)
from note_cast.utils import PasswordManager


class PublishRel(StructuredRel):
    date = DateTimeProperty(default_now=True)


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


class Podcast(StructuredNode, ExternalIDsMixin, MediaAssetsMixin):
    p_id = StringProperty(required=True, index=True)
    p_title = StringProperty(required=True, index=True)
    description = StringProperty()

    category = RelationshipTo(Category, "CATEGORIZED_UNDER")
    episodes = RelationshipFrom("Episode", "PUBLISHED_FOR")

    def to_dict(self) -> dict:
        return {
            "p_id": self.p_id,
            "p_title": self.p_title,
            "itunes_id": self.itunes_id,
            "spotify_id": self.spotify_id,
            "podchaser_id": self.podchaser_id,
        }


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
    def podcast(self):
        return self.published_for.single()

    def to_dict(self, include_podcast: bool = False) -> dict:
        result = {
            "e_id": self.e_id,
            "e_title": self.e_title,
            "audio_url": self.audio_url,
            "length_s": self.length_s,
            "num": self.num,
            "description": self.description,
        }
        if include_podcast:
            result.update({"podcast": self.published_for.single().to_dict()})

        return result


class Quote(StructuredNode):
    q_id = StringProperty(required=True, unique_index=True)
    transcript = StringProperty()
    visible = BooleanProperty(default=True)

    mentioned_on = RelationshipTo(Episode, "MENTIONED_ON", model=MentionRel)
    attachments = RelationshipFrom("Note", "ATTACHED_TO")
    bookmarked_by = RelationshipFrom("User", "BOOKMARKED", cardinality=ZeroOrMore)
    
    @property
    def episode(self):
        return self.mentioned_on.single()

    def to_dict(self) -> dict:
        return {
            "q_id": self.q_id,
            "transcript": self.transcript,
            "visible": self.visible,
        }


class Note(StructuredNode):
    n_id = UniqueIdProperty()
    text = StringProperty(required=True)
    is_public = BooleanProperty(default=False)

    author = RelationshipFrom("User", "ANNOTATED", model=AnnotateRel, cardinality=One)
    attach_to = RelationshipTo("Quote", "ATTACHED_TO")

    @property
    def writer(self):
        """ return author single node"""
        return self.author.single()

    @property
    def quote(self):
        return self.attach_to.single()

    def to_dict(
        self, include_author: bool = False, include_quote: bool = False
    ) -> dict:
        result = {
            "n_id": self.n_id,
            "text": self.text,
            "is_public": self.is_public,
        }
        if include_author:
            result.update({"author": self.author.single().to_dict()})
        if include_quote:
            result.update({"quote": self.quote.single().to_dict()})

        return result


class User(StructuredNode):
    u_id = UniqueIdProperty()
    username = StringProperty(unique=True, required=True)
    email: object = EmailProperty(required=True, unique_index=True)
    password_hash = StringProperty(required=True)
    disabled = BooleanProperty(default=False)
    joined_date = DateTimeProperty(default_now=True)

    notes = RelationshipTo(
        "Note", "ANNOTATED", model=AnnotateRel, cardinality=ZeroOrMore
    )
    bookmarks = RelationshipTo("Quote", "BOOKMARKED", cardinality=ZeroOrMore)

    def to_dict(self) -> dict:
        return {
            "u_id": self.u_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "disabled": self.disabled,
            "joined_date": self.joined_date,
        }

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, plain_password):
        self.password_hash = PasswordManager.generate_password_hash(plain_password)

    def verify_password(self, plain_password):
        return PasswordManager.check_password_hash(plain_password, self.password_hash)
