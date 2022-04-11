from fastapi import APIRouter, Request, Response, status
from note_cast.api.errors import CustomHTTPException
from note_cast.db.crud.quote import QuoteQuery
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.services.cloudinary_api.resource import CloudinaryResource
from note_cast.services.cloudinary_api.uploader import (CloudinaryUpload,
                                                        async_upload)
from tasks.scheduler import cancel_scheduled_job

router = APIRouter(prefix="/callback", tags=["callback"])


@router.post("/cloudinary/upload/")
async def cloudinary_upload_callback(request: Request):

    notification_r = await request.json()

    try:

        if (notification_type := notification_r.get("notification_type")) == "upload":
            # TODO fix for when async is false but performed async due to duration
            if async_upload:
                custom_context = notification_r["context"]["custom"]

                CloudinaryUpload.prep_transcription_job_on_completed_upload(
                    q_id=custom_context["q_id"],
                    p_id=custom_context["p_id"],
                    e_id=custom_context["e_id"],
                    audio_segment_url=notification_r["url"],
                )

        elif notification_type == "info":
            if (
                notification_r["info_kind"] == "google_speech"
                and notification_r["info_status"] == "complete"
            ):

                public_id: str = notification_r["public_id"]
                job_id = public_id.split("/")[-1]
                cancel_scheduled_job(job_id=job_id)

                transcript_public_id = public_id + ".transcript"

                transcript = CloudinaryResource.fetch_transcript(
                    public_id=transcript_public_id, resource_type="raw"
                )

                _ = QuoteQuery.update_transcript(q_id=job_id, transcript=transcript)

    except KeyError as k_err:
        loguru_app_logger.exception(k_err)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as exc:
        loguru_app_logger.exception(exc)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_200_OK)
