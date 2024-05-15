from contextlib import asynccontextmanager

from databases import Database
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(
    app: FastAPI,
    db: Database,
):
    async with db:
        yield
    await db.disconnect()
