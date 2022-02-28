"""Book models."""

import typing

import pydantic
import sqlmodel

from app.models import mixins

if typing.TYPE_CHECKING:
    from app.models.patron import Patron, PatronRead


class BookBase(sqlmodel.SQLModel, mixins.ProposalMixin, mixins.LinksMixin):
    """Base Book model."""
    title_orig: str
    title_en: str
    title_it: str | None
    author: str
    release_year: int | None
    pages: pydantic.PositiveInt | None
    notes: str | None


class Book(BookBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Book database model."""

    patron: "Patron" = sqlmodel.Relationship(back_populates="books")


class BookCreate(BookBase):
    """Book create model."""


class BookRead(BookBase):
    """Book base model."""
    id: pydantic.UUID4


class BookReadWithPatron(BookRead):
    patron: "PatronRead" = None


class BookUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Book update model."""
    title_orig: str | None
    title_en: str | None
    title_it: str | None
    author: str
    release_year: int | None
    pages: pydantic.PositiveInt | None
    notes: str | None
