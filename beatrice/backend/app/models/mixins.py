"""Mixins."""

import datetime

import pydantic
import sqlmodel


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
    proposed_by: int = sqlmodel.Field(foreign_key="patron.id")


class LinksMixin(pydantic.BaseModel):
    """Mixin that defines links and download-related fields.

    Attributes:
        links: A formatted list of links.
    """
    links: str | None
