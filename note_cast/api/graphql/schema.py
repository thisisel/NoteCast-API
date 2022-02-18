from strawberry import Schema

from .queries import Query

graphql_schema = Schema(query=Query)
