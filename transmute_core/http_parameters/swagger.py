from swagger_schema import BodyParameter, QueryParameter, HeaderParameter, PathParameter
from ..function.signature import NoDefault
from .param_set import Param, ParamSet


def get_swagger_parameters(parameters, context):
    ret_parameters = []
    for name, param in parameters.query.items():
        arginfo = param.arginfo
        params = {
            "name": name,
            "description": param.description,
            "required": arginfo.default is NoDefault,
            "collectionFormat": "multi",
        }
        params.update(context.serializers.to_json_schema(arginfo.type))
        ret_parameters.append(QueryParameter(params))

    for name, param in parameters.header.items():
        arginfo = param.arginfo
        params = {
            "name": name,
            "description": param.description,
            "required": arginfo.default is NoDefault,
        }
        params.update(context.serializers.to_json_schema(arginfo.type))
        ret_parameters.append(HeaderParameter(params))

    body_param = _build_body_schema(context.serializers, parameters.body)
    if body_param is not None:
        ret_parameters.append(body_param)

    for name, param in parameters.path.items():
        arginfo = param.arginfo
        params = {
            "name": name,
            "description": param.description,
            "required": arginfo.default is NoDefault,
        }
        params.update(context.serializers.to_json_schema(arginfo.type))
        ret_parameters.append(PathParameter(params))

    return ret_parameters


def _build_body_schema(serializer, body_parameters):
    """body is built differently, since it's a single argument no matter what."""
    description = ""
    if isinstance(body_parameters, Param):
        schema = serializer.to_json_schema(body_parameters.arginfo.type)
        description = body_parameters.description
        required = True
    else:
        if len(body_parameters) == 0:
            return None
        required = set()
        body_properties = {}
        for name, param in body_parameters.items():
            arginfo = param.arginfo
            body_properties[name] = serializer.to_json_schema(arginfo.type)
            body_properties[name]["description"] = param.description
            if arginfo.default is NoDefault:
                required.add(name)
        schema = {
            "type": "object",
            "required": list(required),
            "properties": body_properties,
        }
        required = len(required) > 0
    return BodyParameter(
        {
            "name": "body",
            "description": description,
            "required": required,
            "schema": schema,
        }
    )
