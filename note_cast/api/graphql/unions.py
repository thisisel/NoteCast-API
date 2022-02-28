import strawberry

from .types import GQApiErrorResponse, GQApiResponse

GQResponse = strawberry.union(
    "GraphqlGeneralResponse", types=(GQApiResponse, GQApiErrorResponse)
)
