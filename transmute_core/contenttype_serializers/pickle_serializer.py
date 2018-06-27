from .interface import ContentTypeSerializer
from ..exceptions import SerializationException
try:
    import cPickle as pickle
except ImportError:
    import pickle


class PickleSerializer(ContentTypeSerializer):

    content_type = ["application/pickle"]

    @staticmethod
    def dump(data):
        """
        should return back a bytes (or string in python 2),
        representation of your object, to be used in e.g. response
        bodies.
        """
        return pickle.dumps(data, protocol=-1)

    @property
    def main_type(self):
        return self.content_type[0]

    @staticmethod
    def load(raw_bytes):
        """
        given a bytes object, should return a base python data
        structure that represents the object.
        """
        try:
            return pickle.loads(raw_bytes)
        except pickle.UnpicklingError as e:
            raise SerializationException(str(e))

    @staticmethod
    def can_handle(content_type_name):
        """
        given a content type, returns true if this serializer
        can convert bodies of the given type.
        """
        return "pickle" in content_type_name
