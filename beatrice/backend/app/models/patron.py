"""Patron (user of the application) models."""

import datetime

import sqlmodel

from app.models import mixins


class PatronBase(sqlmodel.SQLModel):
    """Base Patron model."""
    username: str = sqlmodel.Field(sa_column_kwargs={"unique": True})
    email: str
    name: str
    is_active: bool = True
    is_superuser: bool = False


class Patron(PatronBase, mixins.TimestampMixin, table=True):
    """Patron database model."""
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    hashed_password: str | None = sqlmodel.Field(default=None)


class PatronCreate(PatronBase, mixins.TimestampMixin):
    """Patron create model."""
    password: str


class PatronRead(PatronBase, mixins.TimestampMixin):
    """Patron read model."""
    id: int


class PatronUpdate(sqlmodel.SQLModel):
    """Patron update model."""
    username: str | None = None
    email: str | None = None
    password: str | None = None
    name: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    updated_at: datetime.datetime
