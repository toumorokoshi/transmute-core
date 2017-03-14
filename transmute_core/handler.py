"""
utilities to help with generating handlers.
"""
from .exceptions import (
    APIException, NoSerializerFound
)
from .function import Response
from six import reraise


def process_result(transmute_func, context, result, exc, content_type):
    """
    process a result:

    transmute_func: the transmute_func function that returned the response.

    context: the transmute_context to use.

    result: the return value of the function, which will be serialized and
            returned back in the API.

    exc: the exception object. For Python 2, the traceback should
         be attached via the __traceback__ attribute. This is done automatically
         in Python 3.

    content_type: the content type that request is requesting for a return type.
                  (e.g. application/json)
    """
    output = None
    code = transmute_func.success_code
    if isinstance(result, Response):
        code = result.code
        result = result.result
    if exc:
        if isinstance(exc, APIException):
            output = {
                "result": "invalid api use: {0}".format(str(exc)),
                "success": False,
            }
            code = exc.code
        else:
            reraise(type(exc), exc, getattr(exc, "__traceback__", None))
    else:
        return_type = transmute_func.get_response_by_code(code)
        if return_type:
            result = context.serializers.dump(return_type, result)
        output = {
            "result": result,
            "success": True
        }
    try:
        content_type = str(content_type)
        serializer = context.contenttype_serializers[content_type]
    except NoSerializerFound:
        serializer = context.contenttype_serializers.default
        content_type = serializer.main_type
    output["code"] = code
    if output["success"]:
        result = context.response_shape.create_body(output)
    else:
        result = output
    body = serializer.dump(result)
    # keeping the return type a dict to
    # reduce performance overhead.
    return {
        "body": body,
        "code": code,
        "content-type": content_type
    }
