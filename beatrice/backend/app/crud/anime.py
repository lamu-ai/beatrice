"""Anime CRUD controller."""

import sqlmodel

from app.crud import base
from app.models import anime


class AnimeCRUD(base.BaseCRUD[anime.Anime, anime.AnimeCreate,
                              anime.AnimeUpdate]):
    """CRUD controller for anime.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    def get_by_title(cls, session: sqlmodel.Session,
                     title: str) -> anime.Anime | None:
        """Gets an anime by their title.

        Args:
            session: The database session.
            title: The anime's title.
        """
        return session.exec(
            sqlmodel.select(
                anime.Anime).where(anime.Anime.title_en == title)).first()
