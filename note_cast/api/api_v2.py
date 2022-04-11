from strawberry.fastapi import GraphQLRouter

from .graphql.schema import graphql_schema


graphql_router = GraphQLRouter(schema=graphql_schema)