class WebTransmuteException(Exception):
    """ base exception """


class ApiException(WebTransmuteException):
    """
    this exception signifies an exception
    with API
    """


class SerializationException(WebTransmuteException):
    """
    this exceptions signifies an exception with
    serializing values.
    """
