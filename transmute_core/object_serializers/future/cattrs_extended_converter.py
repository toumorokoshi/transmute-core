from cattr import Converter
from typing import List

class ExtendedConverter(Converter):

    def structure(self, obj, cl):
        if isinstance(cl, list):
            cl = List[cl[0]]
        return super(ExtendedConverter, self).structure(obj, cl)

    def unstructure(self, obj, cl):
        if isinstance(cl, list):
            cl = List[cl[0]]
        return super(ExtendedConverter, self).unstructure(obj, cl)
