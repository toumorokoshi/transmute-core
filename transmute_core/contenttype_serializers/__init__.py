from .interface import ContentTypeSerializer
from .json_serializer import JsonSerializer
from .yaml_serializer import YamlSerializer
from .serializer_set import SerializerSet, NoSerializerFound


def get_default_serializer_set():
    return SerializerSet([
        JsonSerializer(),
        YamlSerializer()
    ])
