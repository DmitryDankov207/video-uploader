from django.http import HttpRequest
from ninja import Router

from .schemas import FeedSchema, VideoSchema
from .tasks import create_video

main_router = Router()
video_router = Router()


@video_router.post('/main-feed')
async def get_feed(
    request: HttpRequest,
    feed_schema: FeedSchema,
) -> dict | list:
    """
    Return recently uploaded videos filtered by request params.
    And ordered by adding date descending.
    """


@video_router.post('/upload')
async def upload_video(
    request: HttpRequest,  # noqa
    video_schema: VideoSchema,
) -> None:
    """
    Used to upload video in async mode.
    """
    create_video.apply_async(kwargs={'video_schema': video_schema})
