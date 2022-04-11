from email import message
import strawberry
from note_cast.security.permissions import IsAuthenticated
from . inputs import QuoteMetadata
from . unions import GQResponse, GQApiErrorResponse, GQApiResponse

# from note_cast.services.cloudinary_api.upload import upload_quote


@strawberry.type
class Mutation:

    #TODO add permissions
    @strawberry.mutation(permission_classes=IsAuthenticated)
    def submit_quote(self, data: QuoteMetadata) -> GQResponse:
        pass
