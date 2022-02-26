"""Anime models."""

import typing

import sqlmodel

from app.models import mixins

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


class Anime(AnimeBase, mixins.TimestampsMixin, table=True):
    """Anime database model."""
    id: int | None = sqlmodel.Field(default=None, primary_key=True)

    patron: "Patron" = sqlmodel.Relationship(back_populates="anime")


class AnimeCreate(AnimeBase):
    """Anime create model."""


class AnimeRead(AnimeBase):
    """Anime base model."""
    id: int


class AnimeReadWithPatron(AnimeRead):
    patron: "PatronRead" = None


class AnimeUpdate(sqlmodel.SQLModel, mixins.LinksMixin):
    """Anime update model."""
    title_en: str | None = None
    title_jp: str | None = None
    season_anime: int | None = None
    year: int | None = sqlmodel.Field(default=None, ge=1900)
    season_year: str | None = None
    notes: str | None = None
