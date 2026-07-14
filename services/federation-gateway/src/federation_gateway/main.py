import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .schema import schema

app = FastAPI(title="GraphQL Federation Gateway", version="1.0")
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
async def health():
    return {"status": "ok"}
