from transmute_core.function.signature import Argument, NoDefault
from transmute_core.http_parameters import get_swagger_parameters
from transmute_core import default_context
from transmute_core.http_parameters import Parameters, Param, ParamSet


def test_swagger_parameters():
    parameters = Parameters(
        query=ParamSet(
            {
                "query": Param(
                    argument_name="query", arginfo=Argument("query", None, int)
                )
            }
        ),
        body=ParamSet(
            {
                "left": Param(
                    argument_name="left", arginfo=Argument("left", NoDefault, int)
                ),
                "right": Param(
                    argument_name="right", arginfo=Argument("right", 2, int)
                ),
            }
        ),
        header=ParamSet(
            {
                "header": Param(
                    argument_name="header", arginfo=Argument("header", NoDefault, int)
                )
            }
        ),
        path=ParamSet(
            {
                "path": Param(
                    argument_name="path", arginfo=Argument("path", NoDefault, int)
                )
            }
        ),
    )
    params = get_swagger_parameters(parameters, default_context)
    params = [p.to_primitive() for p in params]
    assert {
        "in": "query",
        "name": "query",
        "required": False,
        "type": "integer",
        "collectionFormat": "multi",
        "description": "",
    } in params
    assert {
        "in": "body",
        "name": "body",
        "schema": {
            "type": "object",
            "required": ["left"],
            "properties": {
                "left": {"type": "integer", "description": ""},
                "right": {"type": "integer", "description": ""},
            },
        },
        "required": True,
        "description": "",
    } in params
    assert {
        "in": "header",
        "name": "header",
        "type": "integer",
        "required": True,
        "description": "",
    } in params
    assert {
        "in": "path",
        "name": "path",
        "type": "integer",
        "required": True,
        "description": "",
    } in params
