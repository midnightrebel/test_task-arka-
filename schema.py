from functools import partial
import strawberry
from strawberry.types import Info
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from consts import SQL
from context_managers import lifespan
from db_context import Context
from settings import db as database


@strawberry.type
class Author:
    name: str


@strawberry.type
class Book:
    id: int
    title: str
    author: Author


@strawberry.type
class Query:
    @strawberry.field
    async def books(
        self,
        info: Info[Context, None],
        author_ids: list[int] | None = [],
        search: str | None = None,
        limit: int | None = None,
    ) -> list[Book]:
        query = SQL
        params: list = []
        conditions: list = []

        if author_ids:
            conditions.append("books.author_id = ANY(%s)")
            params.append(author_ids)

        if search:
            conditions.append("(books.title ILIKE %s OR books.description ILIKE %s)")
            search_term = f"%{search}%"
            params.extend([search_term, search_term])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if limit:
            query += " LIMIT %s"
            params.append(limit)

        result = await info.context.db.fetch_all(query, *params)

        books = [
            Book(
                id=record["id"],
                title=record["title"],
                author=Author(name=record["name"]),
            )
            for record in result
        ]

        return books


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(  # type: ignore
    schema,
    context_getter=partial(Context, database),
)

app = FastAPI(lifespan=partial(lifespan, db=database))
app.include_router(graphql_app, prefix="/graphql")
