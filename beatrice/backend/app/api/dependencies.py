"""Dependencies definitions."""

from fastapi import security, status
from jose import jwt
import fastapi
import jose
import sqlmodel

from app.core import config
from app.core import database
from app.core import security as appsecurity
from app.models import patron as patronmodel
from app.models import token as tokenmodel

oauth2_scheme = security.OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/login/token")

optional_oauth2_scheme = security.OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/login/token", auto_error=False)


def get_session():
    """Yields the database session."""
    with sqlmodel.Session(database.engine) as session:
        yield session


async def get_current_patron(
        session: sqlmodel.Session = fastapi.Depends(get_session),
        token: str = fastapi.Depends(oauth2_scheme)) -> patronmodel.Patron:
    """Returns the current authenticated patron.

    Args:
        session: The database session.
        token: The token used for authentication.
    """
    credentials_exception = fastapi.HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token,
                             config.settings.SECRET_KEY,
                             algorithms=[appsecurity.ALGORITHM])
        subject: str = payload.get("sub")

        if subject is None:
            raise credentials_exception

        token_data = tokenmodel.TokenPayload(subject=subject)
    except jose.JWTError as subject_missing:
        raise credentials_exception from subject_missing

    patron = session.exec(
        sqlmodel.select(patronmodel.Patron).where(
            patronmodel.Patron.username == token_data.subject)).first()

    if patron is None:
        raise credentials_exception

    return patron


async def get_current_patron_or_none(
        session: sqlmodel.Session = fastapi.Depends(get_session),
        token: str = fastapi.Depends(optional_oauth2_scheme)
) -> patronmodel.Patron | None:
    """Returns the current authenticated patron or `None`.

    Args:
        session: The database session.
        token: The token used for authentication.
    """
    if token is not None:
        return await get_current_patron(session, token)

    return None


async def get_current_active_patron(
        current_patron: patronmodel.Patron = fastapi.Depends(get_current_patron)
) -> patronmodel.Patron:
    """Returns the current user if active.

    Args:
        current_patron: The current authenticated patron.
    """
    if not current_patron.is_active:
        raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="You must have an active account")

    return current_patron


async def get_current_active_superuser(
        current_patron: patronmodel.Patron = fastapi.Depends(get_current_patron)
) -> patronmodel.Patron:
    """Returns the current user if superuser.

    Args:
        current_patron: The current authenticated patron.
    """
    if not current_patron.is_superuser:
        raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="You do not have enough privileges")

    return current_patron
