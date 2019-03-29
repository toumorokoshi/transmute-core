"""
utilities to help with generating handlers.
"""
import attr
from .exceptions import APIException, NoSerializerFound
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
    if isinstance(result, Response):
        response = result
    else:
        response = Response(
            result=result, code=transmute_func.success_code, success=True
        )
    if exc:
        if isinstance(exc, APIException):
            response.result = str(exc)
            response.success = False
            response.code = exc.code
        else:
            reraise(type(exc), exc, getattr(exc, "__traceback__", None))
    else:
        return_type = transmute_func.get_response_by_code(response.code)
        if return_type:
            response.result = context.serializers.dump(return_type, response.result)
    try:
        content_type = str(content_type)
        serializer = context.contenttype_serializers[content_type]
    except NoSerializerFound:
        serializer = context.contenttype_serializers.default
        content_type = serializer.main_type
    if response.success:
        result = context.response_shape.create_body(attr.asdict(response))
        response.result = result
    else:
        response.result = attr.asdict(response)
    body = serializer.dump(response.result)
    # keeping the return type a dict to
    # reduce performance overhead.
    return {
        "body": body,
        "code": response.code,
        "content-type": content_type,
        "headers": response.headers,
    }
