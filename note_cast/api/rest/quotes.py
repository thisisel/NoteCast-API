from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Request
from note_cast.api.errors.custom_exceptions import CloudinaryUploadException
from note_cast.schemas import BaseNote

from note_cast.schemas.response import (
    ApiBaseResponse,
    ApiErrorResponse,
)
from note_cast.schemas.user import BaseUserPydantic
from note_cast.security.login_manager import manager
from note_cast.core.dependencies import user_query_params

router = APIRouter(prefix="/quotes")


@router.get(
    "/",
    responses={
        200: {"model": List[BaseNote]},
        200: {"model": BaseNote},
        404: {"model": ApiErrorResponse},
    },
    description="read all quotes or search based on the episode id",
    tags=["quotes"],
)
def read_quotes(e_id: str = Query(None)):

    ...


@router.get("/{q_id}", description="read a single quote", tags=["quotes"])
def read_quote(q_id: str = Path(..., description="quote id of the requested notes")):
    ...


@router.put(
    "/{q_id}",
    description="update a particular quote with a ['bookmark'] reaction",
    tags=["quotes"],
)
def update_bookmark_quote(
    q_id: str = Path(..., description="quote id of the requested notes"),
    user=Depends(manager),
):
    ...


@router.get(
    "/{q_id}/notes",
    description="read all the notes about a particular quote",
    tags=["notes"],
)
def read_notes(
    q_id: str = Path(..., description="quote id of the requested notes"),
    author_username: str = Query(None),
):
    ...


@router.get(
    "/{q_id}/notes/{n_id}",
    description="read a single note about a particular quote",
    tags=["notes"],
)
def read_note(
    q_id: str = Path(..., description="quote id of the requested notes"),
    n_id: str = Path(...),
    author: dict = Depends(user_query_params),
):
    ...


@router.put(
    "/{q_id}/notes/{n_id}",
    description="update with a reaction ['like' | 'comment'] to particular note",
    tags=["notes"],
)
def update_note_reaction(
    q_id: str = Path(..., description="quote id of the requested notes"),
    n_id: str = Path(...),
    user=Depends(manager),
):
    ...
