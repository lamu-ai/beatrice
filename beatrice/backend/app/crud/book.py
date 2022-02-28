"""Book CRUD controller."""

import sqlmodel

from app.crud import base
from app.models import book


class BookCRUD(base.BaseCRUD[book.Book, book.BookCreate, book.BookUpdate]):
    """CRUD controller for book.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    def get_by_title(cls, session: sqlmodel.Session,
                     title: str) -> book.Book | None:
        """Gets a book by their title.

        Args:
            session: The database session.
            title: The book's title.
        """
        return session.exec(
            sqlmodel.select(
                book.Book).where(title in (book.Book.title_orig,
                                           book.Book.title_en,
                                           book.Book.title_it))).first()
