"""Movie models."""

import datetime
import typing

import pydantic
import sqlmodel

from app.models import mixins
from app.models import validators

if typing.TYPE_CHECKING:
    from app.models.patron import Patron, PatronRead


class MovieBase(sqlmodel.SQLModel, mixins.ProposalMixin, mixins.LinksMixin):
    """Base Movie model."""
    title_orig: str
    title_en: str
    title_it: str | None
    release_date: datetime.date | None
    running_time: pydantic.PositiveInt | None
    notes: str | None

    _normalize_title = pydantic.validator("title_orig",
                                          "title_en",
                                          "title_it",
                                          allow_reuse=True)(
                                              validators.normalize_title)


class Movie(MovieBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Movie database model."""

    patron: "Patron" = sqlmodel.Relationship(
        back_populates="movies", sa_relationship_kwargs={"lazy": "selectin"})


class MovieCreate(MovieBase):
    """Movie create model."""


class MovieRead(MovieBase):
    """Movie base model."""
    id: pydantic.UUID4


class MovieReadWithPatron(MovieRead):
    """Movie read model with related patron."""
    patron: "PatronRead" = None


class MovieUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Movie update model."""
    # TODO: Set default to None when
    # https://github.com/tiangolo/sqlmodel/issues/230 is resolved.
    title_orig: str | None = ""
    title_en: str | None = ""
    title_it: str | None = ""
    release_date: datetime.date | None = None
    running_time: pydantic.PositiveInt | None = None
    notes: str | None = None

    _normalize_title = pydantic.validator("title_orig",
                                          "title_en",
                                          "title_it",
                                          allow_reuse=True)(
                                              validators.normalize_title)
