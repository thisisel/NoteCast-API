from ..models import Note, User, Quote, Note
from datetime import datetime


class NoteQuery:
    @classmethod
    def find_single_note(cls, n_id: str) -> Note:
        return Note.nodes.first_or_none(n_id=n_id)

    @classmethod
    def create_note_with_attachments(
        cls, text: str, is_public: bool, author: User, quote: Quote
    ) -> Note:
        note: Note = Note(text=text, is_public=is_public).save()
        note.author.connect(author, {"date_created": datetime.utcnow()})
        note.attach_to.connect(quote)

        return note

    @classmethod
    def update_note(cls, note: Note, text: str, is_public: bool):
        note.text = text
        note.is_public = is_public
        note.save()
        note.refresh()

        return note

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
