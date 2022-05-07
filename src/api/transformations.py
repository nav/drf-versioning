import typing
import abc


class BaseTransformation(abc.ABC):
    DEPRECATION_WARNINGS_KEY = "deprecations"
    REMOVAL_NOTICES_KEY = "removals"

    def __init__(self):
        self.removal_notices = []
        self.deprecation_warnings = []

    def set_deprecation_warning(self, warning):
        self.deprecation_warnings.append(warning)

    def set_removal_notice(self, notice):
        self.removal_notices.append(notice)

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
            typing.Dict[str, typing.Any],
            typing.List[typing.Dict[str, typing.Any]],
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
        if not any(pat.match(endpoint) for pat in self.endpoints):
            return response_body

        response_body = self.process_response_body(response_body)
        metadata = response_body.get("metadata", dict())

        # Insert deprecation warnings and removal notices
        metadata[self.DEPRECATION_WARNINGS_KEY] = self.deprecation_warnings
        metadata[self.REMOVAL_NOTICES_KEY] = self.removal_notices

        response_body["metadata"] = metadata
        return response_body
