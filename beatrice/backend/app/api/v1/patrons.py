"""Patron endpoints."""

from typing import List
import http

from fastapi import responses
from fastapi import status
import fastapi
import sqlmodel

from app.api import dependencies
from app.core import security
from app.crud import patron as patron_crud
from app.models import patron as patron_model
from app.models import response

router = fastapi.APIRouter()


@router.post("/",
             response_model=patron_model.PatronRead,
             status_code=201,
             responses={
                 401: {
                     "model": response.Response
                 },
                 409: {
                     "model": response.Response
                 }
             })
def create_patron(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    patron_in: patron_model.PatronCreate,
    current_patron: patron_model.Patron | None = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_patron_or_none),
) -> patron_model.Patron:
    """Creates a new patron."""
    if current_patron is not None:
        return responses.RedirectResponse(url="/")
    patron_db = patron_crud.PatronCRUD.get_by_username(session,
                                                       patron_in.username)

    if patron_db:
        raise fastapi.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A patron with this username already exists in the system.",
        )

    #if settings.EMAILS_ENABLED and patron_in.email:
    #    send_new_account_email(email_to=patron_in.email,
    #                           username=patron_in.email,
    #                           password=patron_in.password)

    patron = patron_crud.PatronCRUD.create(
        session,
        model_in=patron_in,
        update={
            "hashed_password": security.get_password_hash(patron_in.password)
        })

    return patron


@router.get("/{patron_id}",
            response_model=patron_model.PatronReadWithMedia,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
def read_patron(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    patron_id: int,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> patron_model.Patron:
    """Returns a patron given the id."""
    patron = patron_crud.PatronCRUD.read(session, patron_id)

    if not patron:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Patron not found.")

    return patron


@router.get("/",
            response_model=List[patron_model.PatronRead],
            responses={401: {
                "model": response.Response
            }})
def read_patron_list(
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    offset: int = 0,
    limit: int = fastapi.Query(default=100, le=100),
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> List[patron_model.Patron]:
    """Returns a list of patrons."""
    return patron_crud.PatronCRUD.read_multi(session,
                                             offset=offset,
                                             limit=limit)


@router.put("/",
            response_model=patron_model.PatronRead,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
def update_patron(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    patron_id: int,
    patron_in: patron_model.PatronUpdate,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_patron),
) -> patron_model.Patron:
    """Updates a patron."""
    patron_db = patron_crud.PatronCRUD.read(session, patron_id)

    if not patron_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Patron not found.")
    if current_patron.id != patron_id:
        raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Cannot update another patron.")

    patron_db = patron_crud.PatronCRUD.update(session,
                                              model_db=patron_db,
                                              model_in=patron_in)

    return patron_db


@router.put("/su_update",
            response_model=patron_model.PatronRead,
            responses={
                401: {
                    "model": response.Response
                },
                404: {
                    "model": response.Response
                }
            })
def update_patron_as_superuser(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    patron_id: int,
    patron_in: patron_model.PatronUpdateAsSuperuser,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_superuser),
) -> patron_model.Patron:
    """Updates a patron as a superuser."""
    patron_db = patron_crud.PatronCRUD.read(session, patron_id)

    if not patron_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Patron not found.")

    patron_db = patron_crud.PatronCRUD.update(session,
                                              model_db=patron_db,
                                              model_in=patron_in)

    return patron_db


@router.delete("/",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={401: {
                   "model": response.Response
               }})
def delete_patron(
    *,
    session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
    patron_id: int,
    current_patron: patron_model.Patron = fastapi.Depends(  # pylint: disable=unused-argument
        dependencies.get_current_active_superuser),
):
    """Deletes a patron."""
    patron_db = patron_crud.PatronCRUD.read(session, patron_id)

    if not patron_db:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Patron not found.")

    patron_crud.PatronCRUD.delete(session, patron_id)

    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT.value)
