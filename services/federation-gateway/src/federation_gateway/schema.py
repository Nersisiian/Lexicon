import strawberry
from .resolvers import Query

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
