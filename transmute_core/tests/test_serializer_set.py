def test_hashing_list_object_serializer(object_serializer_set):
    """
    a the object serializer set should supported
    a list object.
    """
    obj = [str]
    object_serializer_set[obj]
    object_serializer_set[obj]
