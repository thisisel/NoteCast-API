from typing import Tuple

from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from note_cast.api.errors import QUOTE_404, CustomHTTPException
from note_cast.db.crud import NoteNode, NoteQuery, UserQuery, QuoteQuery, User
from note_cast.schemas import (
    ApiBaseResponse,
    ApiErrorResponse,
    BaseEpisode,
    BaseNote,
    BaseUserPydantic,
    CreateNote,
    NoteCollection,
    QuoteMetadata,
    SingleNote,
)
from note_cast.security.login_manager import manager
from note_cast.utils.dependencies.core import pagination_params
from note_cast.utils.dependencies.notes import check_get_note_existence_and_permission

router = APIRouter(prefix="/notes")


@router.get(
    "/",
    responses={
        200: {"model": ApiBaseResponse},
        401: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
)
def read_profile_notes_collection(
    user: User = Depends(manager),
    pagination_params: dict = Depends(pagination_params),
):
    notes = UserQuery.find_user_notes_all(user=user, **pagination_params)

    annotations = []
    for note in notes:
        episode_pydantic = BaseEpisode(**note.quote.episode.to_dict())

        quote_pydantic = QuoteMetadata(**note.quote.to_dict())
        quote_pydantic.episode = episode_pydantic

        note_pydantic = BaseNote(
            **note.to_dict(),
        )
        note_pydantic.quote = quote_pydantic
        annotations.append(note_pydantic)

    result: NoteCollection = NoteCollection(
        author=BaseUserPydantic(**user.to_dict()), notes=annotations
    )

    return ApiBaseResponse(
        message="Profile notes were retrieved successfully", data=result
    )


@router.post(
    "/",
    responses={
        201: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
    description="Add note on an existing quote",
)
def create_note(
    user=Depends(manager),
    q_id: str = Body(..., description="existing quote id"),
    new_note_data: CreateNote = Body(...),
):
    if (quote := QuoteQuery.get_quote_by_id(q_id=q_id)) is None:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            category=QUOTE_404,
            detail="Requested Quote does not exist",
        )

    new_note: NoteNode = NoteQuery.create_note_on_quote(
        **new_note_data.dict(), author=user, quote=quote
    )

    user_pydantic: BaseUserPydantic = BaseUserPydantic(**user.to_dict())
    episode_pydantic = BaseEpisode(**quote.episode.to_dict())
    quote_pydantic = QuoteMetadata(**quote.to_dict(), episode=episode_pydantic)
    new_note_pydantic: SingleNote = SingleNote(
        **new_note.to_dict(), author=user_pydantic, quote=quote_pydantic
    )

    result = ApiBaseResponse(
        message="Note was added successfully", data=new_note_pydantic
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(result)
    )


@router.get(
    "/{n_id}",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
        401: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
)
def read_profile_single_note(
    note_user: Tuple[NoteNode, User] = Depends(check_get_note_existence_and_permission),
):
    user_pydantic: BaseUserPydantic = BaseUserPydantic(**note_user[1].to_dict())
    quote_pydantic = QuoteMetadata(**note_user[0].quote.to_dict())
    result: SingleNote = SingleNote(
        **note_user[0].to_dict(), author=user_pydantic, quote=quote_pydantic
    )

    return ApiBaseResponse(message="note retrieved successfully", data=result)


@router.put(
    "/{n_id}",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
        401: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
)
def update_profile_note(
    note_user: Tuple[NoteNode, User] = Depends(check_get_note_existence_and_permission),
    update_data: CreateNote = Body(...),
):
    updated_note = NoteQuery.update_note(note=note_user[0], **update_data.dict())
    quote_pydantic = QuoteMetadata(**note_user[0].quote.to_dict())
    result: SingleNote = SingleNote(
        **updated_note.to_dict(), author=BaseUserPydantic(**note_user[1].to_dict())
    )
    result.quote = quote_pydantic
    return ApiBaseResponse(message="note updated successfully", data=result)


@router.delete(
    "/{n_id}",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
)
def delete_profile_note(
    note_user: Tuple[NoteNode, User] = Depends(check_get_note_existence_and_permission)
):
    note_user[0].delete()

    user_pydantic: BaseUserPydantic = BaseUserPydantic(**note_user[1].to_dict())
    quote_pydantic = QuoteMetadata(**note_user[0].quote.to_dict())
    result: SingleNote = SingleNote(
        **note_user[0].to_dict(), author=user_pydantic, quote=quote_pydantic
    )

    return ApiBaseResponse(message="note deleted successfully", data=result)
