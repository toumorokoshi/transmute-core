"""
utilities to help with generating handlers.
"""
from .exceptions import (
    APIException, NoSerializerFound
)


def process_result(transmute_func, context, result, exc, content_type):
    """ process a result """
    output = None
    code = 200
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
        if transmute_func.return_type:
            result = context.serializers.dump(
                transmute_func.return_type, result
            )
        output = {
            "result": result,
            "success": True
        }
    try:
        serializer = context.contenttype_serializers[content_type]
    except NoSerializerFound:
        serializer = context.contenttype_serializers.default
        content_type = serializer.main_type
    output["code"] = code
    body = serializer.dump(output)
    # keeping the return type a dict to
    # reduce performance overhead.
    return {
        "body": body,
        "code": code,
        "content-type": content_type
    }
