"""Manga models."""

import typing
import datetime

import pydantic
import sqlmodel

from app.models import mixins

if typing.TYPE_CHECKING:
    from app.models.patron import Patron, PatronRead


class MangaBase(sqlmodel.SQLModel, mixins.ProposalMixin, mixins.LinksMixin):
    """Base Manga model."""
    title_en: str
    title_jp: str | None
    volumes: pydantic.NonNegativeInt | None
    chapters: pydantic.PositiveInt | None
    start_date: datetime.date | None
    end_date: datetime.date | None
    notes: str | None

    @pydantic.validator("start_date", "end_date")
    @classmethod
    def check_dates(
        cls, date: datetime.date, values: dict[str, datetime.date]
    ) -> datetime.date:  # pylint: disable=no-self-argument
        assert date >= datetime.date(1900, 1,
                                     1), "The date must be after 1900-01-01"
        if values.get("start_date", None):  # `date` in this case is `end_date`
            assert values[
                "start_date"] <= date, \
                "The end date cannot precede the start date"
        return date


class Manga(MangaBase, mixins.TimestampsMixin, table=True):
    """Manga database model."""
    id: int | None = sqlmodel.Field(default=None, primary_key=True)

    patron: "Patron" = sqlmodel.Relationship(back_populates="manga")


class MangaCreate(MangaBase):
    """Manga create model."""


class MangaRead(MangaBase):
    """Manga base model."""
    id: int


class MangaReadWithPatron(MangaRead):
    patron: "PatronRead" = None


class MangaUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Manga update model."""
    title_en: str | None = None
    title_jp: str | None = None
    volumes: int | None = None
    chapters: int | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    notes: str | None = None
