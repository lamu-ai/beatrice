"""Manga CRUD controller."""

import sqlmodel
from sqlmodel.ext.asyncio import session as aio_session

from app.crud import base
from app.models import manga


class MangaCRUD(base.BaseCRUD[manga.Manga, manga.MangaCreate,
                              manga.MangaUpdate]):
    """CRUD controller for manga.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    async def get_by_title(cls, session: aio_session.AsyncSession,
                           title: str) -> manga.Manga | None:
        """Gets a manga by their title.

        Args:
            session: The database session.
            title: The manga's title.
        """
        manga_list = await session.exec(
            sqlmodel.select(manga.Manga).where(manga.Manga.title_en == title))

        return manga_list.first()
