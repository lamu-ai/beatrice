"""Base CRUD controller."""

import abc
from typing import Any, Dict, Generic, get_args, List, TypeVar

import sqlmodel

ModelType = TypeVar("ModelType", bound=sqlmodel.SQLModel)
CreateModelType = TypeVar("CreateModelType", bound=ModelType)
UpdateModelType = TypeVar("UpdateModelType", bound=ModelType)


class BaseCRUD(Generic[ModelType, CreateModelType, UpdateModelType],
               metaclass=abc.ABCMeta):
    """Base CRUD controller.

    It contains default Create, Read, Update, Delete (CRUD) methods.
    """

    @classmethod
    def create(cls,
               session: sqlmodel.Session,
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
        session.commit()
        session.refresh(model_db)

        return model_db

    @classmethod
    def read(cls, session: sqlmodel.Session, model_id: Any) -> ModelType | None:
        """Reads a model given its id.

        Args:
            session: The database session.
            model_id: The model id.

        Returns:
            A model or None if the model could not be found.
        """
        return session.get(get_args(cls.__orig_bases__[0])[0], model_id)

    @classmethod
    def read_multi(cls,
                   session: sqlmodel.Session,
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
        return session.exec(
            sqlmodel.select(get_args(
                cls.__orig_bases__[0])[0]).offset(offset).limit(limit)).all()

    @classmethod
    def update(cls, session: sqlmodel.Session, *, model_db: ModelType,
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
        session.commit()
        session.refresh(model_db)

        return model_db

    @classmethod
    def delete(cls, session: sqlmodel.Session, model_id: Any):
        """Deletes a model.

        Args:
            session: The database session.
            model_id: The id of the model.
        """
        model_db = session.get(get_args(cls.__orig_bases__[0])[0], model_id)

        session.delete(model_db)
        session.commit()
