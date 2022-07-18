import sys
from datetime import datetime

from django.utils import timezone
from pydantic import BaseModel, conbytes, conint, validator


class ContentSizeExceededException(ValueError):
    """Raise when content size exceeds limit."""


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

    MAX_CONTENT_SIZE = 1024 * 1024 * 7  # 7Mb

    content: conbytes(max_length=MAX_CONTENT_SIZE)  # type: ignore

    @validator('page')
    def content_size_is_valid(cls, value: bytes) -> bytes:
        if sys.getsizeof(value) > cls.MAX_CONTENT_SIZE:
            raise ContentSizeExceededException('Content ')
        return value
