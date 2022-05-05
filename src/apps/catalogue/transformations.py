import re
import typing
from api.transformations import BaseTransformation


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

        self.set_deprecation_warning(
            (
                "You are using a really old version of API. Considering "
                "upgrading to stable version."
            )
        )
        return response_body
