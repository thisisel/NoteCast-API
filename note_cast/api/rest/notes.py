from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query, Request
from note_cast.api.errors.custom_exceptions import CloudinaryUploadException
from note_cast.db.crud import (
    EpisodeNode,
    EpisodeQuery,
    PodcastNode,
    PodcastQuery,
    QuoteNode,
    QuoteQuery,
)
from note_cast.schemas import (
    BaseNote,
    EpisodePydantic,
    NotePydantic,
    PodcastPydantic,
    QuoteMetadata,
    QuotePydantic,
)
from note_cast.schemas.helpers import quote_timestamp_to_mentionrel
from note_cast.schemas.response import (
    ApiBaseResponse,
    ApiErrorResponse,
    CloudinarySuccessResponse,
)
from note_cast.security.login_manager import manager
from note_cast.services.cloudinary_api.uploader import CloudinaryUpload
from interface import schedule_transcript_job
from note_cast.core.dependencies import fetch_quote

router = APIRouter(prefix="/notes")







# @router.post("/quotes")
# async def create_annotation(
#     # user=Depends(manager),
#     quote_node : QuoteNode = Depends(fetch_quote)
# ):


#     return ApiBaseResponse(status=True, message="Quote was fetched", detail=quote_node.__dict__)


@router.get(
    "/",
    responses={
        200: {"model": List[BaseNote]},
        200: {"model": BaseNote},
        404: {"model": ApiErrorResponse},
    },
)
def read_notes(q_id: str = Query(None, description="note id")):
    # if user.isAuthenticated and note.author = user -> return private, public, draft notes
    # else
    # return public notes
    ...
