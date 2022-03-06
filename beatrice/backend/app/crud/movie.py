"""Movie CRUD controller."""

import sqlmodel
from sqlmodel.ext.asyncio import session as aio_session

from app.crud import base
from app.models import movie


class MovieCRUD(base.BaseCRUD[movie.Movie, movie.MovieCreate,
                              movie.MovieUpdate]):
    """CRUD controller for movie.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    async def get_by_title(cls, session: aio_session.AsyncSession,
                           title: str) -> movie.Movie | None:
        """Gets a movie by their title.

        Args:
            session: The database session.
            title: The movie's title.
        """
        movies = await session.exec(
            sqlmodel.select(movie.Movie).where(title in (movie.Movie.title_orig,
                                                         movie.Movie.title_en,
                                                         movie.Movie.title_it)))

        return movies.first()
