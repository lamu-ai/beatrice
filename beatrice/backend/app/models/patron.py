"""Patron (user of the application) models."""

from typing import List
import typing

import pydantic
import sqlmodel

from app.models import mixins

if typing.TYPE_CHECKING:
    from app.models.anime import Anime, AnimeRead
    from app.models.manga import Manga, MangaRead


def capitalize_name(name: str):
    """Capitalizes every word of the input.

    Params:
        name: The name.
    Returns:
        The stripped and capitalized name.
    """
    return name.strip().title()


class PatronBase(sqlmodel.SQLModel):
    """Base Patron model."""
    username: pydantic.constr(strip_whitespace=True,
                              regex=r"^[a-z][_a-z0-9]*$") = sqlmodel.Field(
                                  sa_column_kwargs={"unique": True})
    email: pydantic.EmailStr
    name: str

    _capitalize_name = pydantic.validator("name", pre=True,
                                          allow_reuse=True)(capitalize_name)


class Patron(PatronBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Patron database model."""
    hashed_password: str | None = None
    is_active: bool = True
    is_superuser: bool = False

    anime: List["Anime"] = sqlmodel.Relationship(back_populates="patron")
    manga: List["Manga"] = sqlmodel.Relationship(back_populates="patron")


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


class PatronUpdate(sqlmodel.SQLModel):
    """Patron update model."""
    username: pydantic.constr(strip_whitespace=True,
                              regex=r"^[a-z][_a-z0-9]*$") | None = None
    email: str | None = None
    password: str | None = None
    name: str | None = None

    _capitalize_name = pydantic.validator("name", pre=True,
                                          allow_reuse=True)(capitalize_name)


class PatronUpdateAsSuperuser(PatronUpdate):
    """Patron update model as a superuser."""
    is_active: bool = True
    is_superuser: bool = False
