from email import message
import strawberry
from note_cast.security.permissions import IsAuthenticated
from . inputs import QuoteMetadata
from . unions import GQResponse, GQApiErrorResponse, GQApiResponse

# from note_cast.services.cloudinary_api.upload import upload_quote


@strawberry.type
class Mutation:

    #TODO add permissions
    # @strawberry.mutation(permission_classes=IsAuthenticated)
    @strawberry.mutation
    def submit_quote(self, data: QuoteMetadata) -> GQResponse:

        # start_offset_s: int = TimestampConverter.timestamp_to_seconds(
        #     data.start_timestamp
        # )
        # end_offset_s: int = TimestampConverter.timestamp_to_seconds(data.end_timestamp)
        # quote_duration: int = end_offset_s - start_offset_s

        # if quote_duration < 30 or quote_duration > 180:
        #     return GQApiErrorResponse(
        #         status=False,
        #         message="A quote duration must be between 30 seconds up to 3 minutes",
        #     )

        # public_id: str = get_random_filename(ext="wav")

        # try:

        #     upload_response = upload_quote(
        #         data=data,
        #         public_id=public_id,
        #         start_offset_s=start_offset_s,
        #         end_offset_s=end_offset_s,
        #     )

        #     if (er_msg := upload_response.get("error", None)) is not None:
        #         return GQApiErrorResponse(status=False, message=f"{er_msg}")

        #     # TODO schedule job

        #     return GQApiResponse(
        #         status=True,
        #         message="New quote was added successfully. Transcription will be availble in no time. ",
        #     )

        # except Exception as ex:
        #     return GQApiErrorResponse(message=f"{ex}")
        pass
