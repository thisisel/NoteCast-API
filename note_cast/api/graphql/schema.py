from strawberry import Schema

from .queries import Query
from .mutations import Mutation

graphql_schema = Schema(query=Query, mutation=Mutation)
