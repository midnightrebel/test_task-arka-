from databases import Database
from strawberry.fastapi import BaseContext


class Context(BaseContext):
    db: Database

    def __init__(
        self,
        db: Database,
    ) -> None:
        self.db = db
