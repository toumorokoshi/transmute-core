class TransmuteCoreException(Exception):
    """base exception"""


class APIException(TransmuteCoreException):
    """
    this exception signifies an exception
    with API
    """

    def __init__(self, message, code=400):
        """code can be overriden, to allow the proper status code."""
        super(APIException, self).__init__(message)
        self.code = code


class SerializationException(APIException):
    """
    this exceptions signifies an exception with
    serializing values.
    """


class NoSerializerFound(TransmuteCoreException):
    """
    raised when a serializer does not exist to handle the
    desired content type.
    """


class InvalidTransmuteDefinition(TransmuteCoreException):
    """
    this exception is raised when an invalid configuration for
    transmute is encountered
    """
