"""Anime endpoints."""

from typing import List
import http

from fastapi import status
import fastapi
import sqlmodel

from app.api import dependencies
from app.crud import anime as anime_crud
from app.models import anime

router = fastapi.APIRouter()


@router.post("/", response_model=anime.AnimeRead, status_code=201)
def create_anime(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    anime_in: anime.AnimeCreate,
) -> anime.Anime:
    """Creates a new anime."""
    anime_db = anime_crud.AnimeCRUD.get_by_title(session, anime_in.title_en)

    if anime_db:
        raise fastapi.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An anime with this title already exists in the system.",
        )

    #if settings.EMAILS_ENABLED and anime_in.email:
    #    send_new_account_email(email_to=anime_in.email,
    #                           username=anime_in.email,
    #                           password=anime_in.password)

    user = anime_crud.AnimeCRUD.create(session, model_in=anime_in)

    return user


@router.get("/{anime_id}", response_model=anime.AnimeRead)
def read_anime(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    anime_id: int,
) -> anime.Anime:
    """Returns a anime given the id."""
    return anime_crud.AnimeCRUD.read(session, anime_id)


@router.get("/", response_model=List[anime.AnimeRead])
def read_anime_list(
        session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
        offset: int = 0,
        limit: int = fastapi.Query(default=100, le=100),
) -> List[anime.Anime]:
    """Returns a list of anime."""
    return anime_crud.AnimeCRUD.read_multi(session, offset=offset, limit=limit)


@router.put("/", response_model=anime.AnimeRead)
def update_anime(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    anime_id: int,
    anime_in: anime.AnimeUpdate,
) -> anime.Anime:
    """Updates a anime."""
    anime_db = anime_crud.AnimeCRUD.read(session, anime_id)

    if not anime_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Anime not found.")

    anime_db = anime_crud.AnimeCRUD.update(session,
                                           model_db=anime_db,
                                           model_in=anime_in)

    return anime_db


@router.delete("/", status_code=204)
def delete_anime(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    anime_id: int,
):
    """Deletes an anime."""
    anime_db = anime_crud.AnimeCRUD.read(session, anime_id)

    if not anime_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Anime not found.")

    anime_crud.AnimeCRUD.delete(session, anime_id)

    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT.value)
