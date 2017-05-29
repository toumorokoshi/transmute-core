from swagger_schema import (
    BodyParameter, QueryParameter, HeaderParameter, PathParameter,
)
from ..function.signature import NoDefault
from ..function.param_set import Param, ParamSet


def get_swagger_parameters(parameters, context):
    ret_parameters = []
    for name, details in parameters.query.items():
        ret_parameters.append(QueryParameter({
            "name": name,
            "required": details.default is NoDefault,
            "type": context.serializers.to_json_schema(details.type)["type"],
        }))

    for name, details in parameters.header.items():
        ret_parameters.append(HeaderParameter({
            "name": name,
            "required": details.default is NoDefault,
            "type": context.serializers.to_json_schema(details.type)["type"],
        }))

    if len(parameters.body):
        body_param = _build_body_schema(context.serializers, parameters.body)
        ret_parameters.append(body_param)

    for name, details in parameters.path.items():
        ret_parameters.append(PathParameter({
            "name": name,
            "required": True,
            "type": context.serializers.to_json_schema(details.type)["type"],
        }))

    return ret_parameters


def _build_body_schema(serializer, body_parameters):
    """ body is built differently, since it's a single argument no matter what. """
    if isinstance(body_parameters, Param):
        schema = serializer.to_json_schema(body_parameters.type)
        required = True
    else:
        required = set()
        body_properties = {}
        for name, details in body_parameters.items():
            body_properties[name] = serializer.to_json_schema(details.type)
            if details.default is NoDefault:
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
