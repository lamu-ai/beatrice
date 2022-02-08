"""Token models."""

import sqlmodel


class Token(sqlmodel.SQLModel):
    access_token: str
    token_type: str


class TokenPayload(sqlmodel.SQLModel):
    subject: str | None = None
