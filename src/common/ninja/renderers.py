import orjson
from django.http import HttpRequest
from ninja.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    media_type = 'application/json'

    def render(
        self, request: HttpRequest, data: dict, *, response_status: int
    ) -> bytes:
        return orjson.dumps(data)
