"""Login endpoints."""

import datetime

from fastapi import security
from fastapi import status
import fastapi
import sqlmodel

from app.api import dependencies
from app.core import config
from app.core import security as appsecurity
from app.crud import patron as patron_crud
from app.models import token

router = fastapi.APIRouter()


@router.post("/token", response_model=token.Token)
async def login_for_access_token(
        session: sqlmodel.Session = fastapi.Depends(dependencies.get_session),
        form_data: security.OAuth2PasswordRequestForm = fastapi.Depends()):
    """Returns the OAuth2 access token for the given login.

    Args:
        session: The database session.
        form_data: The OAuth2 form data.
    """
    user = patron_crud.PatronCRUD.authenticate(session,
                                               username=form_data.username,
                                               password=form_data.password)

    if not user:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = appsecurity.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
