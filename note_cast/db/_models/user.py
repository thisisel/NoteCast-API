from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
from typing import Union
from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    EmailProperty,
    BooleanProperty,
    DateTimeProperty,
    RelationshipTo,
    ZeroOrMore,
)

from note_cast.log.custom_logging import loguru_app_logger
from note_cast.utils import PasswordManager
from .relationships import AnnotateRel

if TYPE_CHECKING:
    from .quote import Quote


class User(StructuredNode):
    u_id = UniqueIdProperty()
    username = StringProperty(unique=True, required=True)
    email: object = EmailProperty(required=True, unique_index=True)
    password_hash = StringProperty(required=True)
    disabled = BooleanProperty(default=False)
    joined_date_db = DateTimeProperty(default_now=True)

    notes = RelationshipTo(
        ".note.Note", "ANNOTATED", model=AnnotateRel, cardinality=ZeroOrMore
    )
    bookmarks = RelationshipTo(".quote.Quote", "BOOKMARKED", cardinality=ZeroOrMore)

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

    @classmethod
    def add_bookmark(cls, user: User, quote: Quote):
        user.bookmarks.connect(quote)

    @classmethod
    def delete_bookmark(cls, q_id: str, user: User) -> Quote:
        if (bookmarked_quote := user.bookmarks.get_or_none()) is not None:
            user.disconnect(bookmarked_quote)
            return bookmarked_quote
        else:
            return None

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
