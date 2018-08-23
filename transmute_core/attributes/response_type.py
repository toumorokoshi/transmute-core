import attr
import copy
from ..compat import string_type
from swagger_schema import Response

# @attr.s
# class ParameterType(object):
#     description =


@attr.s
class ResponseType(object):
    type = attr.ib()
    description = attr.ib(
        validator=[attr.validators.instance_of(string_type)], default=""
    )
    headers = attr.ib(
        validator=[attr.validators.instance_of(dict)], default=attr.Factory(dict)
    )
    type_description = attr.ib(default="")

    def swagger_definition(self, context):
        if self.type is not None:
            type_definition = context.serializers.to_json_schema(self.type)
            schema = context.response_shape.swagger(copy.deepcopy(type_definition))
        else:
            schema = {"type": "object"}
        headers = {}

        for name, header in self.headers.items():
            header_definition = context.serializers.to_json_schema(header["type"])
            if "description" in header:
                header_definition["description"] = header["description"]
            headers[name] = header_definition

        if self.type_description:
            schema["description"] = self.type_description
        response = {"description": self.description, "schema": schema}

        if headers:
            response["headers"] = headers

        return Response(response)
