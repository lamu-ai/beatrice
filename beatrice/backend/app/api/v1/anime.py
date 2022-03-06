"""Anime endpoints."""

import http
from typing import List

import fastapi
import pydantic
from fastapi import status
from sqlmodel.ext.asyncio import session as aio_session

from app.api import dependencies
from app.crud import anime as anime_crud
from app.models import anime as anime_model
from app.models import patron as patron_model
from app.models import response

router = fastapi.APIRouter()


@router.post("/",
             response_model=anime_model.AnimeRead,
             status_code=201,
             responses={
                 401: {
                     "model": response.Response
                 },
                 409: {
                     "model": response.Response
                 }
             })
async def create_anime(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    anime_in: anime_model.AnimeCreate,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> anime_model.Anime:
    """Creates a new anime."""
    anime_db = await anime_crud.AnimeCRUD.get_by_title(session,
                                                       anime_in.title_en)

    if anime_db:
        raise fastapi.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An anime with this title already exists in the system.",
        )
    if current_patron.id != anime_in.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    anime = await anime_crud.AnimeCRUD.create(session, model_in=anime_in)

    return anime


@router.get("/{anime_id}",
            response_model=anime_model.AnimeReadWithPatron,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def read_anime(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    anime_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> anime_model.Anime:
    """Returns an anime given the id."""
    anime = await anime_crud.AnimeCRUD.read(session, anime_id)

    if not anime:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Anime not found.")

    return anime


@router.get("/",
            response_model=List[anime_model.AnimeRead],
            responses={401: {
                "model": response.Response
            }})
async def read_anime_list(
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    offset: int = 0,
    limit: int = fastapi.Query(default=100, le=100),
) -> List[anime_model.Anime]:
    """Returns a list of anime."""
    return await anime_crud.AnimeCRUD.read_multi(session,
                                                 offset=offset,
                                                 limit=limit)


@router.put("/",
            response_model=anime_model.AnimeRead,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def update_anime(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    anime_id: pydantic.UUID4,
    anime_in: anime_model.AnimeUpdate,
) -> anime_model.Anime:
    """Updates an anime."""
    anime_db = await anime_crud.AnimeCRUD.read(session, anime_id)

    if not anime_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Anime not found.")
    if current_patron.id != anime_db.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    anime_db = await anime_crud.AnimeCRUD.update(session,
                                                 model_db=anime_db,
                                                 model_in=anime_in)

    return anime_db


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
async def delete_anime(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    anime_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_superuser),
):
    """Deletes an anime."""
    anime_db = await anime_crud.AnimeCRUD.read(session, anime_id)

    if not anime_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Anime not found.")

    await anime_crud.AnimeCRUD.delete(session, anime_id)

    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT.value)
