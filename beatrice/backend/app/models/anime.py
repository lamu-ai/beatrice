"""Anime models."""

import datetime

import sqlmodel

from app.models import mixins


class AnimeBase(sqlmodel.SQLModel, mixins.TimestampsMixin):
    """Base Anime model."""
    title_en: str
    title_jp: str | None
    season_anime: int | None
    year: int | None = sqlmodel.Field(default=None, ge=1900)
    season_year: str | None
    notes: str | None


class Anime(AnimeBase, table=True):
    """Anime database model."""
    id: int | None = sqlmodel.Field(default=None, primary_key=True)


class AnimeCreate(AnimeBase):
    """Anime create model."""


class AnimeRead(AnimeBase):
    """Anime base model."""
    id: int


class AnimeUpdate(sqlmodel.SQLModel):
    """Anime update model."""
    title_en: str | None = None
    title_jp: str | None = None
    season_anime: int | None = None
    year: int | None = None
    season_year: str | None = None
    notes: str | None = None
    link: str | None = None
    updated_at: datetime.datetime
