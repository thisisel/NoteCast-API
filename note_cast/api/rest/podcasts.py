from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query
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


router = APIRouter(prefix="/p")


@router.get(
    "/",
    responses={
        200: {"model": List[PodcastPydantic]},
        200: {"model": PodcastPydantic},
        404: {"model": ApiErrorResponse},
    },
)
def read_podcasts(
    p_id: Optional[str] = Query(None, description="podcast id on notelist")
):
    ...


@router.get(
    "/e",
    responses={
        200: {"model": List[EpisodePydantic]},
        200: {"model": EpisodePydantic},
        404: {"model": ApiErrorResponse},
    },
)
def read_episodes(
    e_id: Optional[str] = Query(None, description="episode id on notelist")
):
    ...


@router.get(
    "/e/q",
    responses={
        200: {"model": List[QuotePydantic]},
        200: {"model": QuotePydantic},
        404: {"model": ApiErrorResponse},
    },
    tags=["quotes"],
)
def read_quotes(q_id: Optional[str] = Query(None, description="quote id")):
    ...


@router.post("/e/q")
def submit_quote(
    # user=Depends(manager),
    data: QuoteMetadata = Body(..., description="required metadata"),
):
    try:

        response = CloudinaryUpload.submit_quote(data=data)
        # from note_cast.services.cloudinary_api.helpers import get_random_filename

        # response = CloudinarySuccessResponse(
        #     status=True,
        #     message="faking cloudinary response",
        #     asset_public_id=get_random_filename(ext="wav"),
        # )  # fake

        if response.status:

            if (podcast := PodcastQuery.get_podcast(p_id=data.p_id)) is None:
                podcast: PodcastNode = PodcastQuery.create_podcast(**data.dict())

            if (
                episode := PodcastQuery.get_related_episode(
                    podcast=podcast, e_id=data.e_id
                )
            ) is None:
                episode: EpisodeNode = EpisodeQuery.create_episode(**data.dict())
                episode.published_for.connect(podcast)

            #TODO check duplicate quote
            quote: QuoteNode = QuoteQuery.create_premature_quote(
                q_id=response.asset_public_id
            )
            quote.mentioned_on.connect(
                episode, quote_timestamp_to_mentionrel(data=data)
            )
            job = schedule_transcript_job(
                seconds=180,
                q_id=response.asset_public_id,
                transcript="test transcription inserted on schedule after 180 seconds",
                job_id=response.asset_public_id,
            )

    except CloudinaryUploadException as ce:
        return ApiErrorResponse(category="external_api_error", message=ce.message)

    except Exception as x:
        print(x)
        return ApiErrorResponse(category="unknown")

    return ApiBaseResponse(**response.dict())


@router.get(
    "/e/q/n",
    responses={
        200: {"model": List[BaseNote]},
        200: {"model": BaseNote},
        404: {"model": ApiErrorResponse},
    },
    tags=["notes"],
)
def read_notes(q_id: Optional[str] = Query(None, description="note id")):
    # if user.isAuthenticated and note.author = user -> return private, public, draft notes
    # else
    # return public notes
    ...
