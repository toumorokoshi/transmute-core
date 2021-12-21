from transmute_core.attributes import TransmuteAttributes, ResponseType
from schematics.types.net import URLType
from swagger_schema import Response


def test_merge():
    left = TransmuteAttributes(methods=["POST"], query_parameters=["a"], tags=["t"])
    right = TransmuteAttributes(
        methods=["PUT"], query_parameters=["b"], body_parameters=["c"]
    )

    joined = left | right

    assert joined.tags == set(["t"])
    assert joined.methods == set(["POST", "PUT"])
    assert joined.query_parameters == set(["a", "b"])
    assert joined.body_parameters == set(["c"])


def test_merge_response_type_by_code():
    left = TransmuteAttributes(
        response_types={200: {"type": bool}, 201: {"type": bool}}
    )
    right = TransmuteAttributes(response_types={201: {"type": str}})
    joined = left | right
    assert joined.response_types == {
        200: ResponseType(type=bool),
        201: ResponseType(type=str),
    }


def test_swagger_definition_if_none(context):
    """a response type that is not specified, should result in a generic swagger schema."""
    response_type = ResponseType(type=None)
    definition = response_type.swagger_definition(context)
    assert definition.to_primitive() == {
        "description": "",
        "schema": {"type": "object"},
    }


def test_header_in_response():
    left = TransmuteAttributes(
        response_types={200: {"type": bool, "headers": {"location": {"type": URLType}}}}
    )
    assert left.response_types == {
        200: ResponseType(type=bool, headers={"location": {"type": URLType}})
    }


def test_merge_response_success_code():
    left = TransmuteAttributes(success_code=200)
    right = TransmuteAttributes(success_code=201)
    joined = left | right
    assert joined.success_code == 201


def test_merge_body_parameters_argument():
    right = TransmuteAttributes()
    left = TransmuteAttributes(body_parameters="body")
    joined = left | right
    assert joined.body_parameters == "body"


def test_duplicate_tags():
    left = TransmuteAttributes(
        methods=["POST"], query_parameters=["a"], tags=["t", "t"]
    )

    assert left.tags == set(["t"])
