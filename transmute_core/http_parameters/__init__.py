from .param_set import Param, ParamSet

class Parameters(object):
    def __init__(self, query=None, body=None, header=None, path=None):
        self.query = query or {}
        self.body = body or {}
        self.header = header or {}
        self.path = path or {}
