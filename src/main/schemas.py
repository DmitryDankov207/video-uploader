from datetime import datetime

from django.utils import timezone
from pydantic import BaseModel, conint, validator


class FeedSchema(BaseModel):
    """
    Validate `api/main-feed` endpoint params.
    """

    DEFAULT_PAGE = 1

    date: datetime | None  # type: ignore
    page: conint(gt=1) | None  # type: ignore

    @validator('date')
    def date_is_empty(cls, value: datetime | None) -> datetime:
        return value or timezone.now()

    @validator('page')
    def page_is_empty(cls, value: int | None) -> int:
        return value or cls.DEFAULT_PAGE


class VideoSchema(BaseModel):
    """
    Validate `api/upload` endpoint payload.
    """

    content: bytes
