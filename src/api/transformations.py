import typing

import abc


class BaseTransformation(abc.ABC):
    API_VERSION_KEY = "api_version"
    DEPRECATION_WARNINGS_KEY = "deprecation_warnings"

    def __init__(self, api_version: str):
        self.api_version = api_version
        self.deprecation_warnings = []

    def set_deprecation_warning(self, warning):
        self.deprecation_warnings.append(warning)

    @abc.abstractmethod
    def process_request_body(self, request_body):
        raise NotImplementedError(
            "Method to produce request body has not been implemented."
        )

    @abc.abstractmethod
    def process_response_body(self, response_body):
        raise NotImplementedError(
            "Method to produce response body has not been implemented."
        )

    def transform_request(
        self,
        endpoint: str,
        request_body: typing.Union[
            typing.Dict[str, typing.Any], typing.List[typing.Dict[str, typing.Any]]
        ],
    ):

        if not any(pat.match(endpoint) for pat in self.endpoints):
            return request_body

        return self.process_request_body(request_body)

    def transform_response(
        self,
        endpoint: str,
        response_body: typing.Union[
            typing.Dict[str, typing.Any], typing.List[typing.Dict[str, typing.Any]]
        ],
    ):
        if (
            not any(pat.match(endpoint) for pat in self.endpoints)
            or "data" not in response_body
        ):
            return response_body

        response_body = self.process_response_body(response_body)
        response_body[self.API_VERSION_KEY] = self.api_version

        # Insert deprecation warnings
        if self.DEPRECATION_WARNINGS_KEY not in response_body:
            response_body[self.DEPRECATION_WARNINGS_KEY] = self.deprecation_warnings

        return response_body
