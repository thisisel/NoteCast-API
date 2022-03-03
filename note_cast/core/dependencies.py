from email import message
from fastapi import Body, Request, status
from fastapi.exceptions import HTTPException
from note_cast.api.errors.custom_exceptions import CloudinaryUploadException
from note_cast.log.custom_logging import loguru_logger
from note_cast.db.crud import (
    PodcastQuery,
    PodcastNode,
    EpisodeNode,
    EpisodeQuery,
    QuoteNode,
    QuoteQuery,
)
from note_cast.schemas import QuoteMetadata
from note_cast.schemas.response import CloudinarySuccessResponse
from note_cast.services.cloudinary_api.uploader import CloudinaryUpload
from note_cast.schemas.helpers import quote_timestamp_to_mentionrel
from interface import schedule_transcript_job


def fetch_quote(data: QuoteMetadata):

    if data.q_id is None:
        return submit_quote(data)
    else:
        return QuoteQuery.read_quote_by_id(q_id=data.q_id)


def submit_quote(data: QuoteMetadata):
    try:

        # response = CloudinaryUpload.upload_quote(data=data)

        from note_cast.services.cloudinary_api.helpers import get_random_filename

        response = CloudinarySuccessResponse(
            status=True,
            message="faking cloudinary response",
            asset_public_id=get_random_filename(ext="wav"),
        )  # fake

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

            quote: QuoteNode = QuoteQuery.create_premature_quote(
                q_id=response.asset_public_id
            )
            quote.mentioned_on.connect(
                episode, quote_timestamp_to_mentionrel(data=data)
            )

            job = schedule_transcript_job(
                seconds=10,
                q_id=response.asset_public_id,
                p_id=data.p_id,
                e_id=data.e_id,
                transcript="test transcription inserted on schedule after 10 seconds",
                job_id=response.asset_public_id,
            )
            return quote

    except CloudinaryUploadException as exc:
        loguru_logger.exception(message=exc.message, errors=exc.error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as exc:
        loguru_logger.exception(exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
