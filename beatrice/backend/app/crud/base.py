"""Base CRUD controller."""

import abc
from typing import Any, Dict, Generic, get_args, List, TypeVar

import sqlmodel
from sqlmodel.ext.asyncio import session as aio_session

ModelType = TypeVar("ModelType", bound=sqlmodel.SQLModel)
CreateModelType = TypeVar("CreateModelType", bound=ModelType)
UpdateModelType = TypeVar("UpdateModelType", bound=ModelType)


class BaseCRUD(Generic[ModelType, CreateModelType, UpdateModelType],
               metaclass=abc.ABCMeta):
    """Base CRUD controller.

    It contains default Create, Read, Update, Delete (CRUD) methods.
    """

    @classmethod
    async def create(cls,
                     session: aio_session.AsyncSession,
                     *,
                     model_in: CreateModelType,
                     update: Dict[str, Any] | None = None) -> ModelType:
        """Creates a new model.

        Args:
            session: The database session.
            model_in: The data used to create the model.

        Returns:
            The ceated model.
        """
        model_db = get_args(cls.__orig_bases__[0])[0].from_orm(model_in, update)

        session.add(model_db)
        await session.commit()
        await session.refresh(model_db)

        return model_db

    @classmethod
    async def read(cls, session: aio_session.AsyncSession,
                   model_id: Any) -> ModelType | None:
        """Reads a model given its id.

        Args:
            session: The database session.
            model_id: The model id.

        Returns:
            A model or None if the model could not be found.
        """
        return await session.get(get_args(cls.__orig_bases__[0])[0], model_id)

    @classmethod
    async def read_multi(cls,
                         session: aio_session.AsyncSession,
                         *,
                         offset: int = 0,
                         limit: int = 100) -> List[ModelType]:
        """Reads the first `limit` models starting at the `offset` position.

        Args:
            session: The database session.
            offset: The starting position at which the database is queried.
            limit: The limit of models to read.

        Returns:
            A list of models.
        """
        models = await session.exec(
            sqlmodel.select(get_args(
                cls.__orig_bases__[0])[0]).offset(offset).limit(limit))

        return models.all()

    @classmethod
    async def update(cls, session: aio_session.AsyncSession, *,
                     model_db: ModelType,
                     model_in: UpdateModelType | Dict[str, Any]) -> ModelType:
        """Updates a model.

        Args:
            session: The database session.
            model_in: The updated model's data.

        Returns:
            The updated model.
        """
        if isinstance(model_in, dict):
            update_data = model_in
        else:
            update_data = model_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(model_db, field, value)

        session.add(model_db)
        await session.commit()
        await session.refresh(model_db)

        return model_db

    @classmethod
    async def delete(cls, session: aio_session.AsyncSession, model_id: Any):
        """Deletes a model.

        Args:
            session: The database session.
            model_id: The id of the model.
        """
        model_db = await session.get(
            get_args(cls.__orig_bases__[0])[0], model_id)

        await session.delete(model_db)
        await session.commit()
