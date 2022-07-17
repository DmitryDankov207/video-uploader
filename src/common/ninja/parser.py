from typing import Any

import orjson
from django.http import HttpRequest
from ninja.parser import Parser


class ORJSONParser(Parser):
    def parse_body(self, request: HttpRequest) -> dict[str, Any]:
        return orjson.loads(request.body)
