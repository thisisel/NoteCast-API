from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from note_cast.db.crud.quote import QuoteQuery
# from note_cast.utils.dependencies.podcasts import podcast_query_params
# from note_cast.utils.dependencies.user import user_query_params
from note_cast.utils.dependencies.query_params import (episode_query_params,
                                                       podcast_query_params,
                                                       quote_query_params,
                                                       user_query_params)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get(
    "/",
    description="search for the notes",
)
def search_notes(
    podcast_q_params: dict = Depends(podcast_query_params),
    episode_q_params: dict = Depends(episode_query_params),
    quote_q_params: dict = Depends(quote_query_params),
    author_q_params: dict = Depends(user_query_params),
):
    if any(podcast_q_params.values()):
        ...
    if any(episode_q_params.values()):
        ...
    if any(quote_q_params.values()):
        ...
    if any(author_q_params.values()):
        ...

@router.get(
    "/{n_id}/",
    description="read a particular note {'n_id'} if visible=True",
)
def read_note_single(n_id: str = Path(...)):
    ...
