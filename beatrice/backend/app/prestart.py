"""Pre-start script."""

import asyncio

from app.core import database


async def check_connection():
    """Checks the connection to the database."""
    # TODO: Find a better way to check connection to the database
    while True:
        try:
            async with database.Session() as session:
                await session.execute("SELECT 1")
                return
        except Exception:  # pylint: disable=broad-except
            pass


if __name__ == "__main__":
    asyncio.run(check_connection())
