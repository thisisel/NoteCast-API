from typing import Optional

from fastapi import Depends, status
from note_cast.api.errors import CustomHTTPException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import NewQuoteMetadata


def upload_quote_on_cloudinary(quote_data: NewQuoteMetadata):
    from note_cast.api.errors.cloudinary_exception import CloudinaryUploadException
    from note_cast.services.cloudinary_api.uploader import CloudinaryUpload

    try:
        
        upload_response = CloudinaryUpload.upload_quote(data=quote_data)
        if upload_response.status:
            return {
                'asset_public_id' : upload_response.asset_public_id,
                'cloudinary_upload_status' : upload_response.data["status"],
                'audio_segment_url' : upload_response.data.get("url"),
            }
    except CloudinaryUploadException as exc:
        loguru_app_logger.exception(exc.message)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as exc:
        loguru_app_logger.exception(exc)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def submit_quote(quote_data: NewQuoteMetadata, quote_upload_response : dict = Depends(upload_quote_on_cloudinary)):
        from note_cast.utils import DataBaseUtils
        from note_cast.services.cloudinary_api.uploader import CloudinaryUpload

        (
            new_quote,
            parent_episode,
            parent_podcast,
        ) = DataBaseUtils.get_or_create_submitting_quote_parents(
            asset_public_id=quote_upload_response.get('asset_public_id'),
            data=quote_data
        )

        if quote_upload_response.get('cloudinary_upload_status') != "pending":

                CloudinaryUpload.prep_transcription_job_on_completed_upload(
                    q_id=quote_upload_response.asset_public_id,
                    p_id=quote_data.p_id,
                    e_id=quote_data.e_id,
                    audio_segment_url=quote_upload_response.get('audio_segment_url'),
                )

        return new_quote, parent_episode, parent_podcast


def quote_query_params(
    #TODO
    # timestamp: MentionRel = Query(None), 
    q_id: Optional[str] = None,
):
    return {"q_id": q_id}
