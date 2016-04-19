import sys
import inspect
from collections import namedtuple

is_py3 = sys.version_info[0] >= 3

FullArgSpec = namedtuple(
    "FullArgSpec",
    ["args", "varargs", "varkw", "defaults",
     "kwonlyargs", "kwonlydefaults", "annotations"]
)


def getfullargspec(func):
    if is_py3:
        return inspect.getfullargspec(func)
    else:
        argspec = inspect.getargspec(func)
        annotations = getattr(func, "__annotations__", {})
        return FullArgSpec(
            argspec.args, argspec.varargs,
            argspec.keywords, argspec.defaults,
            [], None, annotations
        )

if is_py3:
    string_type = str
else:
    string_type = basestring


# From six
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):  # noqa

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})
