"""Movie models."""

import datetime
import typing

import pydantic
import sqlmodel

from app.models import mixins

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


class Movie(MovieBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Movie database model."""

    patron: "Patron" = sqlmodel.Relationship(back_populates="movies")


class MovieCreate(MovieBase):
    """Movie create model."""


class MovieRead(MovieBase):
    """Movie base model."""
    id: pydantic.UUID4


class MovieReadWithPatron(MovieRead):
    patron: "PatronRead" = None


class MovieUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Movie update model."""
    title_orig: str | None
    title_en: str | None
    title_it: str | None
    release_date: datetime.date | None
    running_time: pydantic.PositiveInt | None
    notes: str | None
