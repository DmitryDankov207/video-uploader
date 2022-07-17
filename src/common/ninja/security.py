from typing import Optional

from django.http import HttpRequest
from ninja.security import APIKeyHeader

from config.settings import SECRET_KEY


class ApiKey(APIKeyHeader):
    param_name = 'X-API-Key'

    def authenticate(
        self,
        request: HttpRequest,
        key: Optional[str],
    ) -> Optional[str]:
        return key if key == SECRET_KEY else None
