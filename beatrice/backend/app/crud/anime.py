"""Anime CRUD controller."""

import sqlmodel
from sqlmodel.ext.asyncio import session as aio_session

from app.crud import base
from app.models import anime


class AnimeCRUD(base.BaseCRUD[anime.Anime, anime.AnimeCreate,
                              anime.AnimeUpdate]):
    """CRUD controller for anime.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    async def get_by_title(cls, session: aio_session.AsyncSession,
                           title: str) -> anime.Anime | None:
        """Gets an anime by their title.

        Args:
            session: The database session.
            title: The anime's title.
        """
        anime_list = await session.exec(
            sqlmodel.select(anime.Anime).where(anime.Anime.title_en == title))
        return anime_list.first()
