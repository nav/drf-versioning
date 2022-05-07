def test_can_create_transformation(transformation):
    endpoint = "/api/products/"
    change_datatype = transformation()
    change_datatype.set_deprecation_warning("This is a deprecation warning")
    change_datatype.set_removal_notice("This is a removal notice")

    request_body = {"is_active": 0}

    # process request
    processed_request_body = change_datatype.transform_request(
        endpoint=endpoint, request_body=request_body
    )

    assert not processed_request_body["is_active"]
    assert str(processed_request_body["is_active"]) == "False"

    response_body = processed_request_body
    processed_response_body = change_datatype.transform_response(
        endpoint=endpoint, response_body=response_body
    )

    assert processed_response_body["is_active"] == 0
