"""
utilities to help with generating handlers.
"""
from .exceptions import (
    APIException, NoSerializerFound
)
from .function import Response


def process_result(transmute_func, context, result, exc, content_type):
    """ process a result """
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
            # TODO: better exception raising,
            # to keep traceback context.
            raise exc
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
