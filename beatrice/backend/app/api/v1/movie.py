"""Movie endpoints."""

import http
from typing import List

import fastapi
import pydantic
from fastapi import status
from sqlmodel.ext.asyncio import session as aio_session

from app.api import dependencies
from app.crud import movie as movie_crud
from app.models import movie as movie_model
from app.models import patron as patron_model
from app.models import response

router = fastapi.APIRouter()


@router.post("/",
             response_model=movie_model.MovieRead,
             status_code=201,
             responses={
                 401: {
                     "model": response.Response
                 },
                 409: {
                     "model": response.Response
                 }
             })
async def create_movie(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    movie_in: movie_model.MovieCreate,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> movie_model.Movie:
    """Creates a new movie."""
    movie_db = await movie_crud.MovieCRUD.get_by_title(session,
                                                       movie_in.title_en)

    if movie_db:
        raise fastapi.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An movie with this title already exists in the system.",
        )
    if current_patron.id != movie_in.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    movie = await movie_crud.MovieCRUD.create(session, model_in=movie_in)

    return movie


@router.get("/{movie_id}",
            response_model=movie_model.MovieReadWithPatron,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def read_movie(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    movie_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> movie_model.Movie:
    """Returns a movie given the id."""
    movie = await movie_crud.MovieCRUD.read(session, movie_id)

    if not movie:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Movie not found.")

    return movie


@router.get("/",
            response_model=List[movie_model.MovieRead],
            responses={401: {
                "model": response.Response
            }})
async def read_movie_list(
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    offset: int = 0,
    limit: int = fastapi.Query(default=100, le=100),
) -> List[movie_model.Movie]:
    """Returns a list of movies."""
    return await movie_crud.MovieCRUD.read_multi(session,
                                                 offset=offset,
                                                 limit=limit)


@router.put("/",
            response_model=movie_model.MovieRead,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
async def update_movie(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
    movie_id: pydantic.UUID4,
    movie_in: movie_model.MovieUpdate,
) -> movie_model.Movie:
    """Updates a movie."""
    movie_db = await movie_crud.MovieCRUD.read(session, movie_id)

    if not movie_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Movie not found.")
    if current_patron.id != movie_db.proposed_by:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="https://www.youtube.com/watch?v=Z4oDZCJMDeY")

    movie_db = await movie_crud.MovieCRUD.update(session,
                                                 model_db=movie_db,
                                                 model_in=movie_in)

    return movie_db


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
async def delete_movie(
    *,
    session: aio_session.AsyncSession = fastapi.Depends(
        dependencies.get_session),
    movie_id: pydantic.UUID4,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_superuser),
):
    """Deletes a movie."""
    movie_db = await movie_crud.MovieCRUD.read(session, movie_id)

    if not movie_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Movie not found.")

    await movie_crud.MovieCRUD.delete(session, movie_id)

    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT.value)
