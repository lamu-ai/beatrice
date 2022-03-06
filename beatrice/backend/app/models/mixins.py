"""Mixins."""

import datetime
import uuid

import pydantic
import sqlmodel


class BaseMixin(pydantic.BaseModel):
    """Base mixin class.

    This mixin contains fields common to all models and, as such,
    should always be inherited from.

    Attributes:
        id: The primary key of the model.
    """
    id: pydantic.UUID4 | None = sqlmodel.Field(default_factory=uuid.uuid4,
                                               primary_key=True,
                                               nullable=False)


class TimestampsMixin(pydantic.BaseModel):
    """Mixin that defines timestamp fields.

    Attributes:
        created_at: A timestamp representing when the object was created.
        updated_at: A timestamp representing when the object was updated.
    """
    created_at: datetime.datetime = sqlmodel.Field(
        default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = sqlmodel.Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.datetime.now})


class ProposalMixin(pydantic.BaseModel):
    """Mixin that defines proposal-related fields.

    Attributes:
        proposed_by: The id of the patron who proposed the media.
    """
    proposed_by: pydantic.UUID4 = sqlmodel.Field(foreign_key="patron.id")


class LinksMixin(pydantic.BaseModel):
    """Mixin that defines links and download-related fields.

    Attributes:
        links: A formatted list of links.
    """
    links: str | None
