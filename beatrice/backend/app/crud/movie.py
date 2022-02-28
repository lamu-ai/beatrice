"""Movie CRUD controller."""

import sqlmodel

from app.crud import base
from app.models import movie


class MovieCRUD(base.BaseCRUD[movie.Movie, movie.MovieCreate,
                              movie.MovieUpdate]):
    """CRUD controller for movie.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    def get_by_title(cls, session: sqlmodel.Session,
                     title: str) -> movie.Movie | None:
        """Gets a movie by their title.

        Args:
            session: The database session.
            title: The movie's title.
        """
        return session.exec(
            sqlmodel.select(
                movie.Movie).where(title in (movie.Movie.title_orig,
                                             movie.Movie.title_en,
                                             movie.Movie.title_it))).first()
