import json
from django import http
from rest_framework import status
from api import versions

API_VERSION_HEADER = "X-API-VERSION"


def version_middleware(get_response):
    def gather_transformations(version: versions.Version):
        transformations = []

        while version is not None:
            transformations.extend(version.transformations)
            version = version.next

        return transformations

    def middleware(request):
        if not request.path.startswith("/api"):
            response = get_response(request)
            return response

        api_version = versions.Version.by_name(
            request.headers.get(API_VERSION_HEADER, versions.Version.get_stable().name)
        )
        setattr(request, "api_version", api_version.name)

        transformations = gather_transformations(api_version)

        # Apply transformations to the request
        reversed_transformations = reversed(transformations)
        request_body = request.body

        if request_body and reversed_transformations:
            request_body = json.loads(request_body)
            for TransformationClass in reversed_transformations:
                transformation = TransformationClass(api_version)
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
            for TransformationClass in reversed_transformations:
                transformation = TransformationClass(api_version)
                response_body = transformation.transform_response(
                    request.path, response_body
                )
            response_body = json.dumps(response_body).encode()

        # JSON dumping and loading is intentional until I figure out a
        # consistent way to encode data. Gotta keep bytes until needed
        if not response_body:
            return response

        return http.HttpResponse(
            response_body.decode("utf-8"),
            status=response.status_code,
            headers=response.headers,
        )

    return middleware
