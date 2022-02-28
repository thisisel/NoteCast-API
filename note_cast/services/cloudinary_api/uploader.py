from note_cast.api.errors.custom_exceptions import CloudinaryUploadException
from note_cast.api.graphql.inputs import QuoteMetadata
from note_cast.schemas.response import CloudinarySuccessResponse
from . helpers import TimestampConverter, get_random_filename
from .conf import notification_url
import cloudinary.uploader


class CloudinaryUpload:
    
    @classmethod
    def _upload_quote(
        cls, data: QuoteMetadata, public_id: str, start_offset_s: int, end_offset_s
    ):
        upload_response = cloudinary.uploader.upload(
            file=data.audio_url,
            resource_type="video",
            public_id=public_id,
            folder=f"listennotes_segments/{data.p_id}/{data.e_id}/",
            raw_convert="google_speech",
            notification_url=notification_url,
            transformation=[
                {"start_offset": str(start_offset_s), "end_offset": str(end_offset_s)}
            ],
            context={
                "p_id": data.p_id,
                "e_id": data.e_id,
                "p_title": data.p_title,
                "e_title": data.e_title,
            },
        )
        return upload_response


    @classmethod
    def submit_quote(cls, data: QuoteMetadata):

        start_offset_s: int = TimestampConverter.timestamp_to_seconds(
            data.start_timestamp
        )
        end_offset_s: int = TimestampConverter.timestamp_to_seconds(data.end_timestamp)
        quote_duration: int = end_offset_s - start_offset_s

        if quote_duration < 30 or quote_duration > 180:
            raise CloudinaryUploadException(
                message="A quote duration must be between 30 seconds up to 3 minutes",
            )

        public_id: str = get_random_filename(ext="wav")

        upload_response = cls._upload_quote(
            data=data,
            public_id=public_id,
            start_offset_s=start_offset_s,
            end_offset_s=end_offset_s,
        )

        if (er_msg := upload_response.get("error", None)) is not None:
            raise CloudinaryUploadException(
                message="Error in upload api response", error=er_msg
            )

        return CloudinarySuccessResponse(
            status=True,
            message="New quote was added successfully. Transcription will be availble in no time. ",
            detail=upload_response,
            asset_public_id=public_id,
        )
