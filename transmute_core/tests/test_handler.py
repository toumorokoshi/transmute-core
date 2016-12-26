import json
import pytest
from transmute_core.handler import process_result
from transmute_core import default_context, APIException

CONTENT_TYPE = "application/json"


class SomeOtherException(Exception):
    pass


def test_process_result_200(complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = None
    output = process_result(
        complex_transmute_func,
        default_context, result,
        exc, CONTENT_TYPE
    )
    assert json.loads(output["body"].decode()) == result
    assert output["code"] == 200
    assert output["content-type"] == CONTENT_TYPE


def test_process_result_api_exception(complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = APIException("foo")
    output = process_result(
        complex_transmute_func,
        default_context, result,
        exc, CONTENT_TYPE
    )
    assert json.loads(output["body"].decode()) == {
        "result": "invalid api use: " + str(exc),
        "success": False,
        "code": 400
    }
    assert output["code"] == 400
    assert output["content-type"] == CONTENT_TYPE


def test_process_general_exception(complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = SomeOtherException("foo")
    with pytest.raises(SomeOtherException):
        process_result(
            complex_transmute_func,
            default_context, result,
            exc, CONTENT_TYPE
        )


def test_unknown_content_type_defaults_to_json(complex_transmute_func):
    result = {"kind": "dog", "age": 5}
    exc = None
    output = process_result(
        complex_transmute_func,
        default_context, result,
        exc, "application/myson"
    )
    assert json.loads(output["body"].decode()) == result
    assert output["content-type"] == "application/json"
