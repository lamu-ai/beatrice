"""Initial database setup."""

import asyncio

from app.core import config
from app.core import database
from app.core import security
from app.crud import patron as patron_crud
from app.models import patron as patron_model


async def create_db_and_tables():
    """Initialises the database."""
    async with database.Session() as session:
        admin = await patron_crud.PatronCRUD.get_by_username(
            session, config.settings.ADMIN_USERNAME)

        if not admin:
            admin = patron_model.Patron(username=config.settings.ADMIN_USERNAME,
                                        email=config.settings.ADMIN_EMAIL,
                                        name=config.settings.ADMIN_NAME,
                                        is_active=True,
                                        is_superuser=True)
            await patron_crud.PatronCRUD.create(
                session,
                model_in=admin,
                update={
                    "hashed_password":
                        security.get_password_hash(
                            config.settings.ADMIN_PASSWORD)
                })


if __name__ == "__main__":
    asyncio.run(create_db_and_tables())
