import pytest
from transmute_core.context import TransmuteContext
from transmute_core.response_shape import ResponseShapeComplex


@pytest.fixture
def context():
    return TransmuteContext(
        response_shape=ResponseShapeComplex
    )


def test_complex_response_shape_in_func(transmute_func, context):
    swagger_op = transmute_func.get_swagger_operation(context=context)
    swagger_op.responses["200"].description == "success"
    swagger_op.responses["200"].schema.to_primitive() == {
        "title": "SuccessObject",
        "type": "object",
        "properties": {
            "result": context.serializers.to_json_schema(transmute_func.return_type),
            "success": {"type": "boolean"},
            "code": {"type": "number"}
        },
        "required": ["success", "result", "code"]
    }
