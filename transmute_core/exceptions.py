class WebTransmuteException(Exception):
    """ base exception """


class APIException(WebTransmuteException):
    """
    this exception signifies an exception
    with API
    """

    def __init__(self, message, code=400):
        """ code can be overriden, to allow the proper status code. """
        super(APIException, self).__init__(message)
        self.code = code


class SerializationException(WebTransmuteException):
    """
    this exceptions signifies an exception with
    serializing values.
    """
