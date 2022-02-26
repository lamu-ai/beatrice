"""Patron (user of the application) models."""

from typing import List, TYPE_CHECKING
import datetime

import sqlmodel

from app.models import mixins

if TYPE_CHECKING:
    from app.models.anime import Anime, AnimeRead


class PatronBase(sqlmodel.SQLModel, mixins.TimestampsMixin):
    """Base Patron model."""
    username: str = sqlmodel.Field(sa_column_kwargs={"unique": True})
    email: str
    name: str
    is_active: bool = True


class Patron(PatronBase, table=True):
    """Patron database model."""
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    hashed_password: str | None = None
    is_superuser: bool = False

    anime: List["Anime"] = sqlmodel.Relationship(back_populates="patron")


class PatronCreate(PatronBase):
    """Patron create model."""
    password: str


class PatronRead(PatronBase):
    """Patron read model."""
    id: int
    is_superuser: bool


class PatronReadWithMedia(PatronRead):
    """Patron read model with related media."""
    anime: List["AnimeRead"] = []


class PatronUpdate(sqlmodel.SQLModel):
    """Patron update model."""
    username: str | None = None
    email: str | None = None
    password: str | None = None
    name: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    updated_at: datetime.datetime
