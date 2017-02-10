from transmute_core.function.attributes import TransmuteAttributes


def test_merge():
    left = TransmuteAttributes(
        methods=["POST"], query_parameters=["a"]
    )
    right = TransmuteAttributes(
        methods=["PUT"], query_parameters=["b"],
        body_parameters=["c"]
    )
    joined = left | right
    assert joined.methods == set(["POST", "PUT"])
    assert joined.query_parameters == set(["a", "b"])
    assert joined.body_parameters == set(["c"])


def test_merge_response_type_by_code():
    left = TransmuteAttributes(response_types={
        200: {"type": bool}, 201: {"type": bool}
    })
    right = TransmuteAttributes(response_types={
        201: {"type": str}
    })
    joined = left | right
    assert joined.response_types == {
        200: {"type": bool}, 201: {"type": str}
    }


def test_merge_response_success_code():
    left = TransmuteAttributes(success_code=200)
    right = TransmuteAttributes(success_code=201)
    joined = left | right
    assert joined.success_code == 201
