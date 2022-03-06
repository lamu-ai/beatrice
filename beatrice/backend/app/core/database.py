"""Database utils and configuration."""

from sqlalchemy import orm
from sqlalchemy.ext import asyncio
from sqlmodel.ext.asyncio import session

from app.core import config

engine = asyncio.create_async_engine(config.settings.DB_URI,
                                     pool_pre_ping=True,
                                     future=True)
Session = orm.sessionmaker(engine,
                           class_=session.AsyncSession,
                           expire_on_commit=False)
