import pytest
from transmute_core.response_shape import (
    ResponseShapeSimple, ResponseShapeComplex
)
from swagger_schema import Schema


@pytest.fixture
def schema():
    return Schema({"type": "number"})


def test_response_shape_simple(schema):
    assert ResponseShapeSimple.create_body({"result": "foo"}) == "foo"
    assert ResponseShapeSimple.swagger(schema).to_primitive() ==\
        schema.to_primitive()


def test_response_shape_complex(schema):
    assert ResponseShapeComplex.create_body({"result": "foo", "code": 200}) ==\
        {"result": "foo", "code": 200}

    assert ResponseShapeComplex.swagger(schema).to_primitive() == {
        "title": "SuccessObject",
        "type": "object",
        "properties": {
            "result": schema.to_primitive(),
            "success": {"type": "boolean"},
            "code": {"type": "number"}
        },
        "required": ["success", "result", "code"]
    }
