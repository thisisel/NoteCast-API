from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from .graphql.schema import graphql_schema
from .rest import auth, callback, notes, profile

rest_api_router = APIRouter(prefix="/rest")

rest_api_router.include_router(auth.router, tags=["auth"])
rest_api_router.include_router(callback.router, tags=["callback"])
rest_api_router.include_router(notes.router, tags=["notes"])
rest_api_router.include_router(profile.router)

graphql_router = GraphQLRouter(schema=graphql_schema)
