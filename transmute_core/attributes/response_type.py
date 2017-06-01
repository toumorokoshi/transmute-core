import attr
from ..compat import string_type

# @attr.s
# class ParameterType(object):
#     description =

@attr.s
class ResponseType(object):
    type = attr.ib()
    description = attr.ib(
        validator=[
            attr.validators.instance_of(string_type)
        ],
        default=""
    )
    # headers = attr.ib(
    #     validators=[
    #     ]
    # )
