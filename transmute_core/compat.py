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
    string_type = str  # noqa
    all_string_types = [str]
else:
    string_type = basestring  # noqa
    all_string_types = [basestring, str, unicode]
