import cloudinary.uploader
from cloudinary.exceptions import Error
from note_cast.api.errors.cloudinary_exception import CloudinaryUploadException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import NewQuoteMetadata, CloudinarySuccessResponse
from note_cast.utils import FileUtils, TimeUtils

from . import async_upload, notification_url, raw_convert


class CloudinaryUpload:
    @classmethod
    def _upload_quote(
        cls,
        data: NewQuoteMetadata,
        public_id: str,
        start_offset_s: int,
        end_offset_s,
    ):
        try:
            params = {
                "file": data.audio_url,
                "resource_type": "video",
                "public_id": public_id,
                "folder": f"listennotes_segments/{data.p_id}/{data.e_id}/",
                "notification_url": notification_url,
                "transformation": [
                    {
                        "start_offset": str(start_offset_s),
                        "end_offset": str(end_offset_s),
                    }
                ],
                "context": {
                    "q_id": public_id,
                    "p_id": data.p_id,
                    "e_id": data.e_id,
                    "p_title": data.p_title,
                    "e_title": data.e_title,
                },
            }

            if async_upload or data.length_s >= 1500:
                params.update({"async": True})

            if raw_convert:
                params.update({"raw_convert": "google_speech"})

            upload_response = cloudinary.uploader.upload(**params)

            return upload_response

        except Error as err:
            loguru_app_logger.exception(err)
            raise err

    @classmethod
    def upload_quote(cls, data: NewQuoteMetadata):

        start_offset_s: int = TimeUtils.timestamp_to_seconds(data.start_timestamp)
        end_offset_s: int = TimeUtils.timestamp_to_seconds(data.end_timestamp)
        quote_duration: int = end_offset_s - start_offset_s

        if quote_duration < 10 or quote_duration > 180:
            raise CloudinaryUploadException(
                message="A quote duration must be between 10 seconds up to 3 minutes",
            )

        public_id: str = FileUtils.get_random_filename(ext="wav")

        try:

            upload_response = cls._upload_quote(
                data=data,
                public_id=public_id,
                start_offset_s=start_offset_s,
                end_offset_s=end_offset_s,
            )

        except Error as err:
            raise CloudinaryUploadException(
                message="Error in Cloudinary upload api response", error=err
            )

        loguru_app_logger.debug(upload_response)

        return CloudinarySuccessResponse(
            status=True,
            message="New quote was added successfully. Transcription will be availble in no time. ",
            data=upload_response,
            asset_public_id=public_id,
        )

    @classmethod
    def prep_transcription_job_on_completed_upload(
        cls,
        q_id: str,
        p_id: str,
        e_id: str,
        audio_segment_url: str,
    ):

        from tasks.piplines import trigger_transcription_fallback
        from tasks.scheduler import schedule_pulling_transcription

        job_params: dict = {
            "q_id": q_id,
            "p_id": p_id,
            "e_id": e_id,
            "transcript": "[TEST]failed to pull transcription scheduled in 150",
            "job_id": q_id,
        }

        if raw_convert:
            job_params.update({"seconds": 150})
            _ = schedule_pulling_transcription(**job_params)

        else:
            trigger_transcription_fallback(
                url=audio_segment_url,
                q_id=q_id,
            )

    # TODO
    @classmethod
    def verify_response_sign(cls):
        raise NotImplementedError
