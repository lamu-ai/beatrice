"""Dependencies definitions."""

import fastapi
import jose
import sqlmodel
from fastapi import security, status
from jose import jwt
from sqlmodel.ext.asyncio import session as aio_session

from app.core import config
from app.core import database
from app.core import security as appsecurity
from app.models import patron as patronmodel
from app.models import token as tokenmodel

oauth2_scheme = security.OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/login/token")

optional_oauth2_scheme = security.OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/login/token", auto_error=False)


async def get_session() -> aio_session.AsyncSession:
    """Yields the database session."""
    async with database.Session() as session:
        yield session


async def get_current_patron(
        session: aio_session.AsyncSession = fastapi.Depends(get_session),
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

    patrons = await session.exec(
        sqlmodel.select(patronmodel.Patron).where(
            patronmodel.Patron.username == token_data.subject))
    patron = patrons.first()

    if patron is None:
        raise credentials_exception

    return patron


async def get_current_patron_or_none(
        session: aio_session.AsyncSession = fastapi.Depends(get_session),
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
