"""Manga endpoints."""

import http
from typing import List

import fastapi
import pydantic
from fastapi import status
from sqlmodel.ext.asyncio import session as aio_session

from app.api import dependencies
from app.crud import manga as manga_crud
from app.models import manga as manga_model
from app.models import patron as patron_model
from app.models import response

router = fastapi.APIRouter()


@router.post("/",
             response_model=manga_model.MangaRead,
             status_code=201,
             responses={
                 401: {
                     "model": response.Response
                 },
                 409: {
                     "model": response.Response
                 }
             })
async def create_manga(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    manga_in: manga_model.MangaCreate,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> manga_model.Manga:
    """Creates a new manga."""
    manga_db = await manga_crud.MangaCRUD.get_by_title(session,
                                                       manga_in.title_en)

    if manga_db:
        raise fastapi.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An manga with this title already exists in the system.",
        )
    if current_patron.id != manga_in.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    manga = await manga_crud.MangaCRUD.create(session, model_in=manga_in)

    return manga


@router.get("/{manga_id}",
            response_model=manga_model.MangaReadWithPatron,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def read_manga(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    manga_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> manga_model.Manga:
    """Returns a manga given the id."""
    manga = await manga_crud.MangaCRUD.read(session, manga_id)

    if not manga:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Manga not found.")

    return manga


@router.get("/",
            response_model=List[manga_model.MangaRead],
            responses={401: {
                "model": response.Response
            }})
async def read_manga_list(
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    offset: int = 0,
    limit: int = fastapi.Query(default=100, le=100),
) -> List[manga_model.Manga]:
    """Returns a list of manga."""
    return await manga_crud.MangaCRUD.read_multi(session,
                                                 offset=offset,
                                                 limit=limit)


@router.put("/",
            response_model=manga_model.MangaRead,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def update_manga(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    manga_id: pydantic.UUID4,
    manga_in: manga_model.MangaUpdate,
) -> manga_model.Manga:
    """Updates a manga."""
    manga_db = await manga_crud.MangaCRUD.read(session, manga_id)

    if not manga_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Manga not found.")
    if current_patron.id != manga_db.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    manga_db = await manga_crud.MangaCRUD.update(session,
                                                 model_db=manga_db,
                                                 model_in=manga_in)

    return manga_db


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
async def delete_manga(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    manga_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_superuser),
):
    """Deletes a manga."""
    manga_db = await manga_crud.MangaCRUD.read(session, manga_id)

    if not manga_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Manga not found.")

    await manga_crud.MangaCRUD.delete(session, manga_id)

    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT.value)
