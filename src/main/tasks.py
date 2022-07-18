from celery import app
from django.utils import timezone

from common.transcoders import VideoTranscoder
from config.celery import Queues

from .schemas import VideoSchema


@app.shared_task(queue=Queues.VIDEO_UPLOAD.value)
def create_video(video_schema: VideoSchema) -> None:
    base_filename = str(timezone.now().timestamp()).replace('.', '')
    # TODO: add model generation. S3 upload and Redis caching.
    with VideoTranscoder(
        base_filename, video_schema.content
    ) as _transcoder:  # noqa
        pass
