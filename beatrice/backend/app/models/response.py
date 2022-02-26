"""Response model."""

import sqlmodel


class Response(sqlmodel.SQLModel):
    detail: str
