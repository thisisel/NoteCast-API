from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime


from neomodel import (
    BooleanProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)

from .relationships import AnnotateRel

if TYPE_CHECKING:
    from .user import User
    from .quote import Quote


class Note(StructuredNode):
    n_id = UniqueIdProperty()
    text = StringProperty(required=True)
    is_public = BooleanProperty(default=False)

    author = RelationshipFrom(
        ".user.User", "ANNOTATED", model=AnnotateRel, cardinality=One
    )
    attach_to = RelationshipTo(".quote.Quote", "ATTACHED_TO")

    @property
    def writer(self) -> User:
        """return author single node"""
        return self.author.single()

    @property
    def quote(self) -> Quote:
        return self.attach_to.single()

    @classmethod
    def create_note_on_quote(
        cls, text: str, is_public: bool, author: User, quote: Quote
    ) -> Note:
        note: Note = Note(text=text, is_public=is_public).save()
        note.author.connect(author, {"date_created": datetime.utcnow()})
        note.attach_to.connect(quote)

        return note

    #TODO
    @classmethod
    def search_and_get_public_notes(
        cls,
        p_id: str = None,
        p_title: str = None,
        e_id: str = None,
        e_title: str = None,
        q_id: str = None,
    ):
        ...

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
