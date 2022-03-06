"""Anime models."""

import typing

import pydantic
import sqlmodel

from app.models import mixins
from app.models import validators

if typing.TYPE_CHECKING:
    from app.models.patron import Patron, PatronRead


class AnimeBase(sqlmodel.SQLModel, mixins.ProposalMixin, mixins.LinksMixin):
    """Base Anime model."""
    title_en: str
    title_jp: str | None
    season_anime: int | None
    year: int | None = sqlmodel.Field(default=None, ge=1900)
    season_year: str | None
    notes: str | None

    _normalize_title = pydantic.validator("title_jp",
                                          "title_en",
                                          allow_reuse=True)(
                                              validators.normalize_title)


class Anime(AnimeBase, mixins.TimestampsMixin, mixins.BaseMixin, table=True):
    """Anime database model."""

    patron: "Patron" = sqlmodel.Relationship(
        back_populates="anime", sa_relationship_kwargs={"lazy": "selectin"})


class AnimeCreate(AnimeBase):
    """Anime create model."""


class AnimeRead(AnimeBase):
    """Anime base model."""
    id: pydantic.UUID4


class AnimeReadWithPatron(AnimeRead):
    """Anime read model with related patron."""
    patron: "PatronRead" = None


class AnimeUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Anime update model."""
    # TODO: Set default to None when
    # https://github.com/tiangolo/sqlmodel/issues/230 is resolved.
    title_en: str | None = ""
    title_jp: str | None = ""
    season_anime: int | None = None
    year: int | None = sqlmodel.Field(default=None, ge=1900)
    season_year: str | None = None
    notes: str | None = None

    _normalize_title = pydantic.validator("title_jp",
                                          "title_en",
                                          allow_reuse=True)(
                                              validators.normalize_title)
