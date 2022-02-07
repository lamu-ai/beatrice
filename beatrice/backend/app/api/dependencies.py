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


def get_session():
    """Yields the database session."""
    with sqlmodel.Session(database.engine) as session:
        yield session


async def get_current_patron(
        session: sqlmodel.Session = fastapi.Depends(get_session),
        token: str = fastapi.Depends(oauth2_scheme)):
    """Returns the current authenticated user.

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
            patronmodel.Patron.username == token_data.subject))

    if patron is None:
        raise credentials_exception

    return patron
