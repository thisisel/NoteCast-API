from typing import Any, Union

from neomodel import Q
from neomodel.exceptions import DoesNotExist
from note_cast.db.models import Episode, MentionRel, Quote
from note_cast.schemas import MentionRel as MentionRelPydantic


class QuoteQuery:
    @classmethod
    def create_premature_quote(cls, q_id: str, **kwargs):
        return Quote(q_id=q_id, visible=False).save()

    @classmethod
    def update_transcript(cls, q_id: str, transcript: str):
        if (quote := Quote.nodes.get_or_none(q_id=q_id)) is not None:

            quote.transcript = transcript
            quote.visible = True
            quote.save()

            return quote

        raise DoesNotExist

    @classmethod
    def get_quote_by_id(cls, q_id: str) -> Union[Quote, None]:
        return Quote.nodes.get_or_none(q_id=q_id)

    @classmethod
    def get_quote_episode_or_none(cls, quote: Quote) -> Episode:
        return quote.mentioned_on.single()

    @classmethod
    def get_quote_mention_timestamp_or_none(
        cls, quote: Quote
    ) -> Union[MentionRel, None]:
        if (parent_episode := cls.get_quote_episode_or_none(quote)) is None:
            return None
        mention_rel: MentionRel = quote.mentioned_on.relationship(parent_episode)

        return mention_rel

    @classmethod
    def find_quote(cls, p_id: str = None, e_id: str = None) -> Quote:
        q = {"p_id": Q(p_id=p_id), "e_id": Q(e_id=e_id)}

        if p_id is not None:
            return Quote.nodes.get_or_none(p_id=p_id)
        elif e_id is not None:
            return Quote.nodes.get_or_none(e_id=e_id)

    @classmethod
    def match_and_get_quote_timestamp(cls, e_id: str, timestamp: MentionRelPydantic):
        
        if(episode := Episode.nodes.get_or_none()) is not None:
        
            for quote in episode.quotes.match():
                return quote
            
