"""Book models."""

import typing

import pydantic
import sqlmodel

from app.models import mixins
from app.models import validators

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

    _normalize_title = pydantic.validator("title_orig",
                                          "title_en",
                                          "title_it",
                                          allow_reuse=True)(
                                              validators.normalize_title)


class Book(BookBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Book database model."""

    patron: "Patron" = sqlmodel.Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"})


class BookCreate(BookBase):
    """Book create model."""


class BookRead(BookBase):
    """Book base model."""
    id: pydantic.UUID4


class BookReadWithPatron(BookRead):
    """Book read model with related patron."""
    patron: "PatronRead" = None


class BookUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Book update model."""
    # TODO: Set default to None when
    # https://github.com/tiangolo/sqlmodel/issues/230 is resolved.
    title_orig: str | None = ""
    title_en: str | None = ""
    title_it: str | None = ""
    author: str | None = None
    release_year: int | None = None
    pages: pydantic.PositiveInt | None = None
    notes: str | None = None

    _normalize_title = pydantic.validator("title_orig",
                                          "title_en",
                                          "title_it",
                                          allow_reuse=True)(
                                              validators.normalize_title)
