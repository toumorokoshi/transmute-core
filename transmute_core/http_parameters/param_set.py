import attr
from ..compat import string_type
from ..exceptions import InvalidTransmuteDefinition


@attr.s
class Param(object):
    """a single parameter object."""

    argument_name = attr.ib()
    description = attr.ib(default="")
    # the actual argument object. this gets populated later.
    arginfo = attr.ib(default=None)

    def __or__(self, other):
        raise InvalidTransmuteDefinition(
            "unable to join a single parameter with any other object."
        )

    def values(self):
        return (self,)

    def __setitem__(self, key, value):
        raise InvalidTransmuteDefinition(
            "unable to add parameter {0} to a single parameter.".format(key)
        )


class ParamSet(dict):
    """
    a param set represents a set of a particular grouping of
    parameters, such as header / query / body / etc.
    """

    def __or__(self, other):
        if not isinstance(other, ParamSet):
            raise TypeError("cannot join ParamSet with a {0}".format(type(other)))
        for name, definition in other.items():
            self[name] = definition
