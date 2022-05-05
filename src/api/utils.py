from django import http
from django.http.request import HttpRequest
from api import config


def version_from_header(request: HttpRequest):
    if config.API_VERSION_HEADER in request.headers:
        api_version = request.headers[config.API_VERSION_HEADER]

        if api_version not in config.API_VERSIONS:
            raise http.HTTPException(
                status_code=400, detail="Invalid version requested"
            )
