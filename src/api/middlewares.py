import json
from django import http
from rest_framework import status
from api import versions


def version_middleware(get_response):
    def gather_transformations(version: versions.Version):
        transformations = []

        current_version = versions.Version.get_stable()
        while current_version != version and current_version is not None:
            transformations.extend(current_version.transformations)
            current_version = current_version.prev
        transformations.extend(version.transformations)

        return transformations

    def middleware(request):
        if not request.path.startswith("/api"):
            response = get_response(request)
            return response

        api_version = versions.Version.from_request(request)
        setattr(request, "api_version", api_version)
        transformations = gather_transformations(api_version)

        # Apply transformations to the request
        request_body = request.body

        if request_body and transformations:
            request_body = json.loads(request_body)
            for TransformationClass in transformations:
                transformation = TransformationClass()
                request_body = transformation.transform_request(
                    request.path, request_body
                )

            request_body = json.dumps(request_body).encode()
            request._body = request_body

        response = get_response(request)
        if (
            status.HTTP_200_OK < response.status_code
            or response.status_code >= status.HTTP_300_MULTIPLE_CHOICES
        ):
            return response

        # Apply tranformations to the response
        response_body = response.content

        if response_body:
            response_body = json.loads(response_body)
            for TransformationClass in transformations:
                transformation = TransformationClass()
                response_body = transformation.transform_response(
                    request.path, response_body
                )
            response_body = json.dumps(response_body).encode()

        if not response_body:
            return response

        return http.HttpResponse(
            response_body.decode("utf-8"),
            status=response.status_code,
            headers=response.headers,
        )

    return middleware
