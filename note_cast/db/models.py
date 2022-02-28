from neomodel import (BooleanProperty, DateTimeProperty, EmailProperty,
                      IntegerProperty, One, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, StructuredRel,
                      UniqueIdProperty, ZeroOrMore)
from note_cast.security.password_utils import PasswordManager


class Category(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    podcasts = RelationshipFrom("Podcast", "CATEGORIZED_UNDER")


class Podcast(StructuredNode):
    p_id = StringProperty(required=True, index=True)
    p_title = StringProperty(required=True, index=True)
    p_listennotes_url = StringProperty(required=True)
    category = RelationshipTo(Category, "CATEGORIZED_UNDER")
    episodes = RelationshipFrom("Episode", "PUBLISHED_FOR")


class PublishRel(StructuredRel):
    date = DateTimeProperty(default_now=True)


class Episode(StructuredNode):
    e_id = StringProperty(required=True, index=True)
    e_title = StringProperty(required=True, index=True)
    e_listennotes_url = StringProperty(required=True)
    audio_url = StringProperty(required=True)
    length_h = IntegerProperty()
    length_m = IntegerProperty()
    length_s = IntegerProperty()
    num = IntegerProperty()
    description = StringProperty()

    published_for = RelationshipTo("Podcast", "PUBLISHED_FOR", model=PublishRel)


class MentionRel(StructuredRel):
    start_offset_h = IntegerProperty(required=True)
    start_offset_m = IntegerProperty(required=True)
    start_offset_s = IntegerProperty(required=True)
    end_offset_h = IntegerProperty(required=True)
    end_offset_m = IntegerProperty(required=True)
    end_offset_s = IntegerProperty(required=True)


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
    ...


class Quote(StructuredNode):
    q_id = StringProperty(required=True, unique_index=True)
    transcript = StringProperty()
    visible = BooleanProperty(default=True)

    mentioned_on = RelationshipTo(Episode, "MENTIONED_ON", model=MentionRel)
    attachments = RelationshipFrom("Note", "ATTACHED_TO")


class Note(StructuredNode):
    n_id = UniqueIdProperty()
    text = StringProperty(required=True)
    is_public = BooleanProperty(default=False)

    author = RelationshipFrom("User", "ANNOTATED", model=AnnotateRel, cardinality=One)
    attach_to = RelationshipTo("Quote", "ATTACHED_TO")


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

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, plain_password):
        self.password_hash = PasswordManager.generate_password_hash(plain_password)

    def verify_password(self, plain_password):
        return PasswordManager.check_password_hash(plain_password, self.password_hash)
