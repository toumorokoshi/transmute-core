from swagger_schema import (
    BodyParameter, QueryParameter, HeaderParameter, PathParameter,
)
from ..function.signature import NoDefault


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
    for name, details in parameters.body.items():
        ret_parameters.append(BodyParameter({
            "name": name,
            "required": details.default is NoDefault,
            "schema": context.serializers.to_json_schema(details.type),
        }))
    for name, details in parameters.path.items():
        ret_parameters.append(PathParameter({
            "name": name,
            "required": True,
            "type": context.serializers.to_json_schema(details.type)["type"],
        }))
    return ret_parameters

def _extract_base_type(context, details):
    """ extract the basic type of the context """
