from note_cast.db.models import Quote

from neomodel.exceptions import DoesNotExist


def pull_transcript(q_id: str, transcript: str):
    if (quote := Quote.nodes.get_or_none(q_id=q_id)) is not None:
        quote.transcript = transcript
        quote.save()
        
        return quote
