"""Manga models."""

import datetime
import typing

import pydantic
import sqlmodel

from app.models import mixins
from app.models import validators

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

    _normalize_title = pydantic.validator("title_jp",
                                          "title_en",
                                          allow_reuse=True)(
                                              validators.normalize_title)

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


class Manga(MangaBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Manga database model."""

    patron: "Patron" = sqlmodel.Relationship(
        back_populates="manga", sa_relationship_kwargs={"lazy": "selectin"})


class MangaCreate(MangaBase):
    """Manga create model."""


class MangaRead(MangaBase):
    """Manga base model."""
    id: pydantic.UUID4


class MangaReadWithPatron(MangaRead):
    """Manga read model with related patron."""
    patron: "PatronRead" = None


class MangaUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Manga update model."""
    # TODO: Set default to None when
    # https://github.com/tiangolo/sqlmodel/issues/230 is resolved.
    title_en: str | None = ""
    title_jp: str | None = ""
    volumes: int | None = None
    chapters: int | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    notes: str | None = None

    _normalize_title = pydantic.validator("title_jp",
                                          "title_en",
                                          allow_reuse=True)(
                                              validators.normalize_title)
