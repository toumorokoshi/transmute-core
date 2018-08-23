import attr
from collections import Mapping


@attr.s
class Response(object):
    result = attr.ib()
    code = attr.ib(default=200)
    headers = attr.ib(
        validator=[attr.validators.instance_of(Mapping)], default=attr.Factory(dict)
    )
    success = attr.ib(validator=[attr.validators.instance_of(bool)], default=True)
