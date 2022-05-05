import re
from api import transformations


def test_can_create_transformation():
    class ChangeDataType(transformations.BaseTransformation):
        """Changes is_active int (0,1) to boolean and vice-versa."""

        endpoints = [re.compile("/api/products")]

        def process_request_body(self, request_body):
            return request_body

        def process_response_body(self, response_body):
            return response_body
