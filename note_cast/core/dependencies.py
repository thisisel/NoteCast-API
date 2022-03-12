from fastapi import Query, status
from fastapi.exceptions import HTTPException
from note_cast.api.errors.custom_exceptions import CloudinaryUploadException
from note_cast.core.settings import settings
from note_cast.db.crud import (
    EpisodeNode,
    EpisodeQuery,
    PodcastNode,
    PodcastQuery,
    QuoteNode,
    QuoteQuery,
)
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import QuoteMetadata
from note_cast.schemas.response import ApiBaseResponse
from note_cast.services.cloudinary_api.uploader import CloudinaryUpload
from note_cast.utils import DataUtils
from tasks.scheduler import schedule_transcript_job
from tasks.piplines import begin_transcribe_fallback


def fetch_quote(data: QuoteMetadata):

    if data.q_id is None:
        return submit_quote(data)
    else:
        return QuoteQuery.read_quote_by_id(q_id=data.q_id)


def submit_quote(data: QuoteMetadata):
    try:

        response = CloudinaryUpload.upload_quote(data=data)

        # from note_cast.services.cloudinary_api.helpers import \
        #     get_random_filename

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

            quote: QuoteNode = QuoteQuery.create_premature_quote(
                q_id=response.asset_public_id
            )
            quote.mentioned_on.connect(
                episode, DataUtils.quote_timestamp_to_mentionrel(data=data)
            )

            job_params: dict = {
                "q_id": response.asset_public_id,
                "p_id": data.p_id,
                "e_id": data.e_id,
                "transcript": "[TEST]failed to pull transcription scheduled in 150 seconds in the absence of notification",
                "job_id": response.asset_public_id,
            }
            if settings.CLOUDINARY_RAW_CONVERT:
                job_params.update({"seconds": 150})
                job = schedule_transcript_job(**job_params)

            else:
                begin_transcribe_fallback(
                    audio_url=response.detail["url"], q_id=response.asset_public_id
                )

            return ApiBaseResponse(
                status=True,
                message="your quote was submitted successfully and the transcription will be ready in o time",
                detail= {'q_id' : response.asset_public_id}
            )

    except CloudinaryUploadException as exc:
        loguru_app_logger.exception(message=exc.message, errors=exc.error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as exc:
        loguru_app_logger.exception(exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_query_params(u_id: str = Query(None), username: str = Query(None)):
    return dict(u_id=u_id, username=username)


def podcast_query_params(
    p_id: str = Query(None),
    p_title: str = Query(None),
    e_id: str = Query(None),
    e_title: str = Query(None),
):
    return dict(p_id=p_id, p_title=p_title, e_id=e_id, e_title=e_title)
