"""Book CRUD controller."""

import sqlmodel
from sqlmodel.ext.asyncio import session as aio_session

from app.crud import base
from app.models import book


class BookCRUD(base.BaseCRUD[book.Book, book.BookCreate, book.BookUpdate]):
    """CRUD controller for book.

    It contains Create, Read, Update, and Delete methods.
    """

    @classmethod
    async def get_by_title(cls, session: aio_session.AsyncSession,
                           title: str) -> book.Book | None:
        """Gets a book by their title.

        Args:
            session: The database session.
            title: The book's title.
        """
        books = await session.exec(
            sqlmodel.select(book.Book).where(title in (book.Book.title_orig,
                                                       book.Book.title_en,
                                                       book.Book.title_it)))
        return books.first()
