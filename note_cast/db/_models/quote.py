from __future__ import annotations
from typing import TYPE_CHECKING

from neomodel import (
    BooleanProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    ZeroOrMore,
    db
)
from neomodel.exceptions import DoesNotExist
from .relationships import MentionRel

if TYPE_CHECKING:
    from .episode import Episode


class Quote(StructuredNode):
    q_id = StringProperty(required=True, unique_index=True)
    transcript = StringProperty()
    visible = BooleanProperty(default=True)

    mentioned_on = RelationshipTo(".episode.Episode", "MENTIONED_ON", model=MentionRel)
    attachments = RelationshipFrom(".note.Note", "ATTACHED_TO")
    bookmarked_by = RelationshipFrom(".user.User", "BOOKMARKED", cardinality=ZeroOrMore)

    @property
    def episode(self) -> Episode:
        return self.mentioned_on.single()

    @property
    def mention_time(self) -> MentionRel:
        return self.mentioned_on.relationship(self.episode)

    @classmethod
    def create_premature_quote(cls, q_id: str):
        """
        Create a hidden quote with no transcription
        Args:
            q_id (str): a unique id given to the new note by caller

        Returns: None

        """
        return cls(q_id=q_id, visible=False).save()

    @classmethod
    def update_transcript(cls, q_id: str, transcript: str):
        if (quote := Quote.nodes.get_or_none(q_id=q_id)) is not None:

            quote.transcript = transcript
            quote.visible = True
            quote.save()

            return quote

        raise DoesNotExist


    @classmethod
    def get_most_annotated_quotes(
        cls, to_dict: bool = False, skip: int = 0, limit: int = 20
    ):

        rows, cols = db.cypher_query(
            "MATCH (:Note)-[a:ATTACHED_TO]->(q:Quote)"
            "RETURN q, count(a) as cite_times"
            "ORDER BY cite_times DESC"
            "SKIP $skip"
            "LIMIT $limit",
            params={"skip": skip, "limit": limit},
        )

        return [
            cls.inflate(r[0]) if not to_dict else cls.inflate(r[0]).to_dict()
            for r in rows
        ]

    #TODO
    @classmethod
    def find_duplicate_quote(cls, timestamp, e_id):
        pass

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
