import re
import pytest
from api import versions
from api import transformations as api_transformations
from catalogue import transformations


@pytest.fixture
def rename_field_transformation():
    return transformations.RenameProductSKUToName


@pytest.fixture
def v1():
    return versions.Version(name="v1", transformations=[])


@pytest.fixture
def v2(v1, rename_field_transformation):
    return versions.Version(
        name="v2",
        transformations=[rename_field_transformation],
        prev=v1,
    )


@pytest.fixture
def transformation():
    class ChangeDataType(api_transformations.BaseTransformation):
        """Changes is_active int (0,1) to boolean and vice-versa."""

        endpoints = [re.compile("/api/products")]

        def process_request_body(self, request_body):
            is_active = request_body.get("is_active", None)
            if is_active is None:
                return request_body

            is_active = bool(is_active)

            request_body["is_active"] = is_active
            return request_body

        def process_response_body(self, response_body):
            is_active = response_body.get("is_active", None)
            if is_active is None:
                return response_body

            is_active = 0 if not is_active else 1
            response_body["is_active"] = is_active
            return response_body

    return ChangeDataType
