from django.http import HttpRequest
from ninja import Router
from schemas import FeedSchema, VideoSchema

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
    request: HttpRequest,
    video_schema: VideoSchema,
) -> None:
    """
    Used to upload video in async mode.
    """
