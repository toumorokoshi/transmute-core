from transmute_core.http_parameters import (
    get_swagger_parameters, ParamSet, Param, Parameters
)
from transmute_core.function.signature import Argument, NoDefault


def test_post_schema_swagger(parameter_post_schema, context):
    assert get_swagger_parameters(parameter_post_schema, context)[0].to_primitive() == {
        "in": "body",
        "name": "body",
        "required": True,
        "schema": {
            "type": "number"
        }
    }


def test_header_only_schema(context):
    params = Parameters(
        path=ParamSet({"path": Param(argument_name="path",
                                     arginfo=Argument("path", NoDefault, int))}),
    )
    assert get_swagger_parameters(params, context)[0].to_primitive() == {
        "in": "path",
        "name": "path",
        "required": True,
        "type": "number"
    }
