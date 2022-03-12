import cloudinary.uploader
from cloudinary.exceptions import Error
from note_cast.api.errors.custom_exceptions import CloudinaryUploadException
from note_cast.api.graphql.inputs import QuoteMetadata
from note_cast.schemas.response import CloudinarySuccessResponse
from note_cast.utils import FileUtils, TimeUtils

from . import notification_url


class CloudinaryUpload:
    @classmethod
    def _upload_quote(
        cls,
        data: QuoteMetadata,
        public_id: str,
        start_offset_s: int,
        end_offset_s,
        raw_convert: bool,
    ):
        try:
            params = {
                # "async": True,
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
                    "p_id": data.p_id,
                    "e_id": data.e_id,
                    "p_title": data.p_title,
                    "e_title": data.e_title,
                },
            }
            if raw_convert:
                params.update({"raw_convert": "google_speech"})

            upload_response = cloudinary.uploader.upload(**params)

            return upload_response

        except Error as err:

            if str(err).split(".")[0] == "Rate Limit Exceeded":
                print("download audio clip and give it to google speech")

            else:
                raise err

    @classmethod
    def upload_quote(cls, data: QuoteMetadata, raw_convert: bool = False):

        start_offset_s: int = TimeUtils.timestamp_to_seconds(
            data.start_timestamp
        )
        end_offset_s: int = TimeUtils.timestamp_to_seconds(data.end_timestamp)
        quote_duration: int = end_offset_s - start_offset_s

        if quote_duration < 30 or quote_duration > 180:
            raise CloudinaryUploadException(
                message="A quote duration must be between 30 seconds up to 3 minutes",
            )
        
        public_id: str = FileUtils.get_random_filename(ext='wav')

        try:

            upload_response = cls._upload_quote(
                data=data,
                public_id=public_id,
                start_offset_s=start_offset_s,
                end_offset_s=end_offset_s,
                raw_convert=raw_convert,
            )

        except Error as err:
            raise CloudinaryUploadException(
                message="Error in Cloudinary upload api response", error=err
            )

        return CloudinarySuccessResponse(
            status=True,
            message="New quote was added successfully. Transcription will be availble in no time. ",
            detail=upload_response,
            asset_public_id=public_id,
        )
