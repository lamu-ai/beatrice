"""Book endpoints."""

import http
from typing import List

import fastapi
import pydantic
from fastapi import status
from sqlmodel.ext.asyncio import session as aio_session

from app.api import dependencies
from app.crud import book as book_crud
from app.models import book as book_model
from app.models import patron as patron_model
from app.models import response

router = fastapi.APIRouter()


@router.post("/",
             response_model=book_model.BookRead,
             status_code=201,
             responses={
                 401: {
                     "model": response.Response
                 },
                 409: {
                     "model": response.Response
                 }
             })
async def create_book(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    book_in: book_model.BookCreate,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> book_model.Book:
    """Creates a new book."""
    book_db = await book_crud.BookCRUD.get_by_title(session, book_in.title_en)

    if book_db:
        raise fastapi.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An book with this title already exists in the system.",
        )
    if current_patron.id != book_in.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    book = await book_crud.BookCRUD.create(session, model_in=book_in)

    return book


@router.get("/{book_id}",
            response_model=book_model.BookReadWithPatron,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def read_book(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    book_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> book_model.Book:
    """Returns a book given the id."""
    book = await book_crud.BookCRUD.read(session, book_id)

    if not book:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Book not found.")

    return book


@router.get("/",
            response_model=List[book_model.BookRead],
            responses={401: {
                "model": response.Response
            }})
async def read_book_list(
        session: aio_session.AsyncSession = fastapi.Depends(
            dependencies.get_session),
        current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
            dependencies.get_current_active_patron),
        offset: int = 0,
        limit: int = fastapi.Query(default=100, le=100),
) -> List[book_model.Book]:
    """Returns a list of books."""
    return await book_crud.BookCRUD.read_multi(session,
                                               offset=offset,
                                               limit=limit)


@router.put("/",
            response_model=book_model.BookRead,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def update_book(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    book_id: pydantic.UUID4,
    book_in: book_model.BookUpdate,
) -> book_model.Book:
    """Updates a book."""
    book_db = await book_crud.BookCRUD.read(session, book_id)

    if not book_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Book not found.")
    if current_patron.id != book_db.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    book_db = await book_crud.BookCRUD.update(session,
                                              model_db=book_db,
                                              model_in=book_in)

    return book_db


@router.delete("/",
               status_code=204,
               responses={
                   401: {
                       "model": response.Response
                   },
                   404: {
                       "model": response.Response
                   }
               })
async def delete_book(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    book_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_superuser),
):
    """Deletes a book."""
    book_db = await book_crud.BookCRUD.read(session, book_id)

    if not book_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Book not found.")

    await book_crud.BookCRUD.delete(session, book_id)

    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT.value)
