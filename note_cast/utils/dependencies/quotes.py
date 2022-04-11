from typing import Optional

from fastapi import status
from note_cast.api.errors import CustomHTTPException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import NewQuoteMetadata
from note_cast.utils import DataBaseUtils


def submit_quote(quote_data: NewQuoteMetadata):
    from note_cast.api.errors.cloudinary_exception import \
        CloudinaryUploadException
    from note_cast.services.cloudinary_api.uploader import CloudinaryUpload

    # from tasks.piplines import trigger_transcription_fallback
    # from tasks.scheduler import schedule_pulling_transcription

    try:

        upload_response = CloudinaryUpload.upload_quote(data=quote_data)

        if upload_response.status:

            new_quote, parent_episode, parent_podcast = DataBaseUtils.get_or_create_submitting_quote_parents(
                data=quote_data, asset_public_id=upload_response.asset_public_id
            )

            # job_params: dict = {
            #     "q_id": upload_response.asset_public_id,
            #     "p_id": quote_data.p_id,
            #     "e_id": quote_data.e_id,
            #     "transcript": "[TEST]failed to pull transcription scheduled in 150",
            #     "job_id": upload_response.asset_public_id,
            # }

            if upload_response.data["status"] != "pending":

                #     if settings.CLOUDINARY_RAW_CONVERT:
                #         job_params.update({"seconds": 150})
                #         job = schedule_pulling_transcription(**job_params)

                #     else:
                #         trigger_transcription_fallback(
                #             audio_url=upload_response.data["url"], q_id=upload_response.asset_public_id
                #         )

                CloudinaryUpload.prep_transcription_job_on_completed_upload(
                    q_id= upload_response.asset_public_id, 
                    p_id= quote_data.p_id,
                    e_id= quote_data.e_id,
                    audio_segment_url=upload_response.data["url"],
                )

            return new_quote, parent_episode, parent_podcast

    except CloudinaryUploadException as exc:
        loguru_app_logger.exception(exc.message)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as exc:
        loguru_app_logger.exception(exc)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



def quote_query_params(
    # timestamp: MentionRel = Query(None),
    q_id : Optional[str] = None,
    ):
    return {'q_id' : q_id}
