import pytest
from transmute_core.http_parameters import Parameters, Param, ParamSet
from transmute_core.function.signature import Argument, NoDefault


@pytest.fixture
def parameters():
    return Parameters(
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


@pytest.fixture
def parameter_post_schema():
    return Parameters(
        body=Param(argument_name="body", arginfo=Argument("left", NoDefault, int))
    )
