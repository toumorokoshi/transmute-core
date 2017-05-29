from transmute_core.http_parameters import get_swagger_parameters


def test_post_schema_swagger(parameter_post_schema, context):
    assert get_swagger_parameters(parameter_post_schema, context)[0].to_primitive() == {
        "in": "body",
        "name": "body",
        "required": True,
        "schema": {
            "type": "number"
        }
    }
