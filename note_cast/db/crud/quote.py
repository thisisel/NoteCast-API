from note_cast.db.models import Quote
from neomodel.exceptions import DoesNotExist


class QuoteQuery:
    @staticmethod
    def create_premature_quote(q_id: str, **kwargs):
        return Quote(q_id=q_id, visible=False).save()

    @staticmethod
    def update_transcript(q_id : str, transcript : str):
        if (quote := Quote.nodes.get_or_none(q_id=q_id)) is not None:
            quote.transcript = transcript
            quote.save()
            print(quote.transcript)
            return quote
        raise DoesNotExist

    @staticmethod
    def read_quote_by_id(q_id : str):
        return Quote.nodes.get_or_none(q_id=q_id)
