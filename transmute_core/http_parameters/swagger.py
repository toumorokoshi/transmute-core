from swagger_schema import (
    BodyParameter, QueryParameter, HeaderParameter, PathParameter,
)
from ..function.signature import NoDefault
from .param_set import Param, ParamSet


def get_swagger_parameters(parameters, context):
    ret_parameters = []
    for name, param in parameters.query.items():
        arginfo = param.arginfo
        ret_parameters.append(QueryParameter({
            "name": name,
            "required": arginfo.default is NoDefault,
            "type": context.serializers.to_json_schema(arginfo.type)["type"],
        }))

    for name, param in parameters.header.items():
        arginfo = param.arginfo
        ret_parameters.append(HeaderParameter({
            "name": name,
            "required": arginfo.default is NoDefault,
            "type": context.serializers.to_json_schema(arginfo.type)["type"],
        }))

    body_param = _build_body_schema(context.serializers, parameters.body)
    if body_param is not None:
        ret_parameters.append(body_param)

    for name, details in parameters.path.items():
        arginfo = param.arginfo
        ret_parameters.append(PathParameter({
            "name": name,
            "required": True,
            "type": context.serializers.to_json_schema(arginfo.type)["type"],
        }))

    return ret_parameters


def _build_body_schema(serializer, body_parameters):
    """ body is built differently, since it's a single argument no matter what. """
    if isinstance(body_parameters, Param):
        schema = serializer.to_json_schema(body_parameters.arginfo.type)
        required = True
    else:
        if len(body_parameters) == 0:
            return None
        required = set()
        body_properties = {}
        for name, param in body_parameters.items():
            arginfo = param.arginfo
            body_properties[name] = serializer.to_json_schema(arginfo.type)
            if arginfo.default is NoDefault:
                required.add(name)
        schema = {
            "type": "object",
            "required": list(required),
            "properties": body_properties
        }
        required = len(required) > 0
    return BodyParameter({
        "name": "body",
        "required": required,
        "schema": schema
    })
