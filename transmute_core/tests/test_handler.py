import json
import pytest
from transmute_core.handler import process_result
from transmute_core import default_context, APIException, Response

CONTENT_TYPE = "application/json"


class SomeOtherException(Exception):
    pass


def test_process_result_200(complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = None
    output = process_result(
        complex_transmute_func, default_context, result, exc, CONTENT_TYPE
    )
    assert json.loads(output["body"].decode()) == result
    assert output["code"] == 200
    assert output["content-type"] == CONTENT_TYPE
    assert output["headers"] == {}


def test_process_result_api_exception(complex_transmute_func):
    result = None
    exc = APIException("foo")
    output = process_result(
        complex_transmute_func, default_context, result, exc, CONTENT_TYPE
    )
    assert json.loads(output["body"].decode()) == {
        "result": str(exc),
        "success": False,
        "code": 400,
        "headers": {},
    }
    assert output["code"] == 400
    assert output["content-type"] == CONTENT_TYPE


def test_process_general_exception(complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = SomeOtherException("foo")
    with pytest.raises(SomeOtherException):
        process_result(
            complex_transmute_func, default_context, result, exc, CONTENT_TYPE
        )


def test_process_custom_code(transmute_func_custom_code):
    output = process_result(
        transmute_func_custom_code, default_context, 20, None, CONTENT_TYPE
    )
    assert output["code"] == 201


def test_process_result_multiple_types(response_transmute_func):
    result = Response("foo", 401)
    output = process_result(
        response_transmute_func, default_context, result, None, CONTENT_TYPE
    )
    assert json.loads(output["body"].decode()) == "foo"
    assert output["code"] == 401

    result = Response(False, 201)
    output = process_result(
        response_transmute_func, default_context, result, None, CONTENT_TYPE
    )
    assert json.loads(output["body"].decode()) is False
    assert output["code"] == 201


@pytest.mark.parametrize("content_type", ["application/myson", None])
def test_unknown_content_type_defaults_to_json(content_type, complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = None
    output = process_result(
        complex_transmute_func, default_context, result, exc, content_type
    )
    assert json.loads(output["body"].decode()) == result
    assert output["content-type"] == "application/json"
