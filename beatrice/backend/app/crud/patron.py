"""Patron CRUD controller."""

from typing import Any, Dict

import sqlmodel
from sqlmodel.ext.asyncio import session as aio_session

from app.core import security
from app.crud import base
from app.models import patron


class PatronCRUD(base.BaseCRUD[patron.Patron, patron.PatronCreate,
                               patron.PatronUpdate]):
    """CRUD controller for patrons.

    It contains Create, Read, Update, and Delete methods and additional
    methods for authentication and read by username.
    """

    @classmethod
    async def update(
            cls, session: aio_session.AsyncSession, *, model_db: patron.Patron,
            model_in: patron.PatronUpdate | Dict[str, Any]) -> patron.Patron:
        """Updates a patron.

        Args:
            session: The database session.
            patron_db: The current patron's data.
            patron_in: The updated patron's data.

        Returns:
            The updated patron.
        """
        if isinstance(model_in, dict):
            update_data = model_in
        else:
            update_data = model_in.dict(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = security.get_password_hash(
                update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return await super().update(session,
                                    model_db=model_db,
                                    model_in=update_data)

    @classmethod
    async def get_by_username(cls, session: aio_session.AsyncSession,
                              username: str) -> patron.Patron | None:
        """Gets a patron by their username.

        Args:
            session: The database session.
            username: The patron's username.

        Returns:
            The patron with the given username.
        """
        patrons = await session.exec(
            sqlmodel.select(
                patron.Patron).where(patron.Patron.username == username))

        return patrons.first()

    @classmethod
    async def authenticate(cls, session: aio_session.AsyncSession, *,
                           username: str, password: str) -> patron.Patron:
        """Authenticates the patron with given username and password.

        Args:
            session: The database session.
            username: The patron's username.
            password: The patron's password.

        Returns:
            The authenticated patron.
        """
        user = await PatronCRUD.get_by_username(session, username)

        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None

        return user
