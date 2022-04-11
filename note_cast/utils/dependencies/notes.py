
from typing import Optional, Tuple


from note_cast.db.crud import NoteQuery, NoteNode, User

from fastapi import Depends, Path, HTTPException, status
from note_cast.security.login_manager import manager


def check_get_note_existence_and_permission(
    n_id: str = Path(...), user: User = Depends(manager)
) -> Tuple[NoteNode, User]:
    if (note := NoteQuery.find_single_note(n_id=n_id)) is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # if note.author.all()[0].username != user.username:
    if note.author.single().username != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return note, user

def note_query_params(
    # date_annotated: datetime.datetime = Query(None),
    n_id : Optional[str] = None,
    ):
    return {'n_id' : n_id}