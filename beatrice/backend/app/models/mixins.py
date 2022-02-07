"""Mixins."""

import datetime

import pydantic


class TimestampMixin(pydantic.BaseModel):
    """Mixin that defines timestamp fields.

    Attributes:
        created_at: A timestamp representing when the object was created.
        updated_at: A timestamp representing when the object was updated.
    """
    created_at: datetime.datetime
    updated_at: datetime.datetime


class LinkMixin(pydantic.BaseModel):
    """Mixin that defines a link field.

    Attributes:
        link: A link.
    """
    link: str
