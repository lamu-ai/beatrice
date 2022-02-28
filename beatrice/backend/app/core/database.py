"""Database utils and configuration."""

import sqlmodel

from app.core import config
from app.models import anime  # pylint: disable=unused-import
from app.models import manga  # pylint: disable=unused-import
from app.models import movie  # pylint: disable=unused-import
from app.models import patron  # pylint: disable=unused-import

engine = sqlmodel.create_engine(config.settings.DB_URI, pool_pre_ping=True)


def create_db_and_tables():
    """Initialises the database."""
    sqlmodel.SQLModel.metadata.drop_all(engine)
    sqlmodel.SQLModel.metadata.create_all(engine)
