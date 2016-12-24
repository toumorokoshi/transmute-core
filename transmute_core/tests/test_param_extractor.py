import pytest
import json
from transmute_core import (
    ParamExtractor, NoArgument,
    describe, annotate, default_context,
    APIException
)
from transmute_core.function import TransmuteFunction


@describe(paths=["/"], query_parameters=["pos"])
@annotate({"pos": str})
def pos_type(pos):
    pass


@describe(paths=["/"])
@annotate({"framework_arg": str})
def with_framework_arg(framework_arg):
    pass


@describe(
    paths=["/"],
    query_parameters=["query"],
    header_parameters=["header"],
    path_parameters=["path"],
    body_parameters=["body"]

)
@annotate({
    "query": str, "header": str, "path": str,
    "body": str
})
def all_param_type(query=1, header=2, path=3, body=4):
    pass


class ParamExtractorMock(ParamExtractor):

    body = json.dumps({"body": "body"})

    def _get_framework_args(self):
        return {
            "framework_arg": "framework_arg"
        }

    def _query_argument(self, key, is_list):
        if is_list:
            return ["query"]
        else:
            return "query"

    def _header_argument(self, key):
        return "header"

    def _path_argument(self, key):
        return "path"


@pytest.fixture
def all_param_type_transmute_func():
    """ ensure retrieval of all parameter types is honored. """
    return TransmuteFunction(all_param_type)


def test_extract_params(all_param_type_transmute_func):

    extractor = ParamExtractorMock()
    args, kwargs = extractor.extract_params(
        default_context, all_param_type_transmute_func,
        "application/json"
    )
    assert args == []
    assert kwargs == {
        "query": "query",
        "header": "header",
        "path": "path",
        "body": "body"
    }


def test_extract_params_no_arguments(all_param_type_transmute_func):
    """ if no arguments are passed, use the defaults """

    extractor = ParamExtractorMock()
    extractor._query_argument = lambda *args: NoArgument
    extractor._header_argument = lambda *args: NoArgument
    extractor._path_argument = lambda *args: NoArgument
    args, kwargs = extractor.extract_params(
        default_context, all_param_type_transmute_func,
        "application/json"
    )
    assert args == []
    assert kwargs == {
        "query": 1,
        "header": 2,
        "path": 3,
        "body": "body"
    }


def test_body_with_only_default_args_can_be_empty(all_param_type_transmute_func):
    """ if no body is passed, and all body args have defaults, it is still a valid request. """

    extractor = ParamExtractorMock()
    extractor.body = ""
    args, kwargs = extractor.extract_params(
        default_context, all_param_type_transmute_func,
        "application/json"
    )
    assert args == []
    assert kwargs == {
        "query": "query",
        "header": "header",
        "path": "path",
        "body": 4,
    }


def test_extract_params_bad_body_content_type(all_param_type_transmute_func):
    """ if no arguments are passed, use the defaults """

    extractor = ParamExtractorMock()
    with pytest.raises(APIException):
        extractor.extract_params(
            default_context, all_param_type_transmute_func,
            "application/myson"
        )


def test_extract_params_positional_args():
    """ if no arguments are passed, use the defaults """
    tf = TransmuteFunction(pos_type)
    extractor = ParamExtractorMock()
    args, kwargs = extractor.extract_params(
        default_context, tf, "application/json"
    )
    assert args == ["query"]
    assert kwargs == {}


def test_with_framework_arg():
    """ """
    tf = TransmuteFunction(with_framework_arg)
    extractor = ParamExtractorMock()
    args, kwargs = extractor.extract_params(
        default_context, tf, "application/json"
    )
    assert args == ["framework_arg"]
    assert kwargs == {}
