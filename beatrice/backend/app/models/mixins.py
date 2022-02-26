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
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProposalMixin(pydantic.BaseModel):
    """Mixin that defines proposal-related fields.

    Attributes:
        proposed_by: The id of the patron who proposed the media.
    """
    proposed_by: int = sqlmodel.Field(default=None, foreign_key="patron.id")
