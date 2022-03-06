"""Patron (user of the application) models."""

from typing import List
import typing

import pydantic
import sqlmodel

from app.models import mixins
from app.models import validators

if typing.TYPE_CHECKING:
    from app.models.anime import Anime, AnimeRead
    from app.models.manga import Manga, MangaRead
    from app.models.movie import Movie, MovieRead
    from app.models.book import Book, BookRead


class PatronBase(sqlmodel.SQLModel):
    """Base Patron model."""
    username: pydantic.constr(strip_whitespace=True,
                              regex=r"^[a-z][_a-z0-9]*$") = sqlmodel.Field(
                                  sa_column_kwargs={"unique": True})
    email: pydantic.EmailStr
    name: str

    _normalize_name = pydantic.validator("name", allow_reuse=True)(
        validators.normalize_name)


class Patron(PatronBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Patron database model."""
    hashed_password: str | None = None
    is_active: bool = True
    is_superuser: bool = False

    anime: List["Anime"] = sqlmodel.Relationship(
        back_populates="patron", sa_relationship_kwargs={"lazy": "selectin"})
    manga: List["Manga"] = sqlmodel.Relationship(
        back_populates="patron", sa_relationship_kwargs={"lazy": "selectin"})
    movies: List["Movie"] = sqlmodel.Relationship(
        back_populates="patron", sa_relationship_kwargs={"lazy": "selectin"})
    books: List["Book"] = sqlmodel.Relationship(
        back_populates="patron", sa_relationship_kwargs={"lazy": "selectin"})


class PatronCreate(PatronBase):
    """Patron create model."""
    password: str


class PatronRead(PatronBase):
    """Patron read model."""
    id: pydantic.UUID4
    is_active: bool
    is_superuser: bool


class PatronReadWithMedia(PatronRead):
    """Patron read model with related media."""
    anime: List["AnimeRead"] = []
    manga: List["MangaRead"] = []
    movies: List["MovieRead"] = []
    books: List["BookRead"] = []


class PatronUpdate(sqlmodel.SQLModel):
    """Patron update model."""
    username: pydantic.constr(strip_whitespace=True,
                              regex=r"^[a-z][_a-z0-9]*$") | None = None
    email: pydantic.EmailStr | None = None
    password: str | None = None
    # TODO: Set default to None when
    # https://github.com/tiangolo/sqlmodel/issues/230 is resolved.
    name: str | None = ""

    _normalize_name = pydantic.validator("name", allow_reuse=True)(
        validators.normalize_name)


class PatronUpdateAsSuperuser(PatronUpdate):
    """Patron update model as a superuser."""
    is_active: bool = True
    is_superuser: bool = False
