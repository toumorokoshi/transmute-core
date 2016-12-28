from transmute_core.function.parameters import Parameters
from transmute_core.function.signature import Argument, NoDefault
from transmute_core.swagger.function import get_swagger_parameters
from transmute_core import default_context


def test_swagger_parameters():
    parameters = Parameters(
        query={"query": Argument("query", None, int)},
        body={"body": Argument("body", NoDefault, int)},
        header={"header": Argument("header", NoDefault, int)},
        path={"path": Argument("path", NoDefault, int)},
    )
    params = get_swagger_parameters(parameters, default_context)
    params = [p.to_primitive() for p in params]
    assert {
        "in": "query",
        "name": "query",
        "required": False,
        "type": "number"
    } in params
    assert {
        "in": "body",
        "name": "body",
        "schema": {"type": "number"},
        "required": True,
    } in params
    assert {
        "in": "header",
        "name": "header",
        "type": "number",
        "required": True,
    } in params
    assert {
        "in": "path",
        "name": "path",
        "type": "number",
        "required": True,
    } in params
