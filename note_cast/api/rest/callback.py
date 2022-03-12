from fastapi import APIRouter, Request, Response, status
from note_cast.services.cloudinary_api.resource import CloudinaryResource
from note_cast.db.crud.quote import QuoteQuery
from tasks.scheduler import cancel_scheduled_job
from note_cast.log.custom_logging import loguru_app_logger

router = APIRouter(prefix="/callback")


@router.post("/cloudinary/upload/")
async def cloudinary_upload_callback(request: Request):

    notification_r = await request.json()

    if (
        notification_r.get("info_kind") == "google_speech"
        and notification_r.get("info_status") == "complete"
    ):

        try:
            public_id: str = notification_r["public_id"]
            job_id = public_id.split("/")[-1]
            cancel_scheduled_job(job_id=job_id)

            transcript_public_id = public_id + ".transcript"

            # resource_info_response = CloudinaryResource.get_resource_info(public_id=raw_public_id, resource_type="raw")
            # r = CloudinaryResource.download_resource(
            #         resource_info_response["url"]
            # )

            # jsn = r.json()
            # transcript = jsn[0]["transcript"]

            transcript = CloudinaryResource.fetch_transcript(
                public_id=transcript_public_id, resource_type="raw"
            )

            quote = QuoteQuery.update_transcript(q_id=job_id, transcript=transcript)

        except Exception as ex:
            print(ex)

    else:
        loguru_app_logger.info(
            f"cloudinary callback notification lacked the key : 'info_kind'\n {notification_r}"
        )

    return Response(status_code=status.HTTP_200_OK)
