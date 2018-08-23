import pytest
from transmute_core.http_parameters import (
    get_swagger_parameters,
    ParamSet,
    Param,
    Parameters,
)
from transmute_core.function.signature import Argument, NoDefault
from datetime import datetime


def test_post_schema_swagger(parameter_post_schema, context):
    assert get_swagger_parameters(parameter_post_schema, context)[0].to_primitive() == {
        "in": "body",
        "name": "body",
        "required": True,
        "description": "",
        "schema": {"type": "integer"},
    }


def test_header_only_schema(context):
    params = Parameters(
        path=ParamSet(
            {
                "path": Param(
                    argument_name="path", arginfo=Argument("path", NoDefault, int)
                )
            }
        )
    )
    assert get_swagger_parameters(params, context)[0].to_primitive() == {
        "in": "path",
        "name": "path",
        "required": True,
        "type": "integer",
        "description": "",
    }


@pytest.mark.parametrize(
    "inp, expected",
    [
        (
            Parameters(
                query=ParamSet(
                    {
                        "query": Param(
                            argument_name="query",
                            arginfo=Argument("query", NoDefault, datetime),
                        )
                    }
                )
            ),
            {
                "in": "query",
                "name": "query",
                "required": True,
                "type": "string",
                "format": "date-time",
                "collectionFormat": "multi",
                "description": "",
            },
        ),
        (
            Parameters(
                path=ParamSet(
                    {
                        "path": Param(
                            argument_name="path",
                            arginfo=Argument("path", NoDefault, datetime),
                        )
                    }
                )
            ),
            {
                "in": "path",
                "name": "path",
                "required": True,
                "type": "string",
                "format": "date-time",
                "description": "",
            },
        ),
        (
            Parameters(
                header=ParamSet(
                    {
                        "path": Param(
                            argument_name="path",
                            arginfo=Argument("path", NoDefault, datetime),
                        )
                    }
                )
            ),
            {
                "in": "header",
                "name": "path",
                "required": True,
                "type": "string",
                "format": "date-time",
                "description": "",
            },
        ),
    ],
)
def test_additional_type_info(context, inp, expected):
    """
    query parameter should have additional type data
    (like format) added to it.
    """
    assert get_swagger_parameters(inp, context)[0].to_primitive() == expected
