class TransmuteAttributes(object):

    def __init__(self, methods=None,
                 query_parameters=None, body_parameters=None,
                 header_parameters=None, path_parameters=None):
        self.methods = set(methods or ["GET"])
        self.query_parameters = query_parameters or []
        self.body_parameters = body_parameters or []
        self.header_parameters = header_parameters or []
        self.path_parameters = path_parameters or []
