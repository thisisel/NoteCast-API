from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from .graphql.schema import graphql_schema
from .rest import auth

rest_api_router = APIRouter(prefix="/rest")

rest_api_router.include_router(auth.router, tags=["auth"])
graphql_router = GraphQLRouter(schema=graphql_schema)
