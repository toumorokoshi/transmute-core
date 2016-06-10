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
else:
    string_type = basestring  # noqa


# From six
# LICENSE for six:
# Copyright (c) 2010-2016 Benjamin Peterson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):  # noqa

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})
