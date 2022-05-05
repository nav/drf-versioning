import re
import typing


class BaseTransformation:
    API_VERSION_KEY = "api_version"
    DEPRECATION_WARNINGS_KEY = "deprecation_warnings"

    def __init__(self, api_version: str):
        self.api_version = api_version
        self.deprecation_warnings = []

    def set_deprecation_warning(self, warning):
        self.deprecation_warnings.append(warning)

    def process_request_body(self):
        raise NotImplementedError(
            "Method to produce request body has not been implemented."
        )

    def process_response_body(self):
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


class RenameProductSKUToName(BaseTransformation):
    endpoints = [re.compile("/api/products.*")]

    def process_request_body(self, request_body: typing.Union[dict, list]):
        def _traverse(alist):
            for adict in alist:
                if "sku" in adict:
                    adict["name"] = adict.pop("sku")
            return alist

        if isinstance(request_body, list):
            request_body = _traverse(request_body)
        else:
            request_body = _traverse([request_body])[0]
        return request_body

    def process_response_body(self, response_body: typing.Union[dict, list]):
        def _traverse(alist):
            for adict in alist:
                if "name" in adict:
                    adict["sku"] = adict.pop("name")
            return alist

        if isinstance(response_body["data"], list):
            response_body["data"] = _traverse(response_body["data"])
        else:
            response_body["data"] = _traverse([response_body["data"]])[0]

        self.set_deprecation_warning("You are using a really old version of API")
        return response_body
