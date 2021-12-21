import json


def test_happy_path(test_app):
    r = test_app.get("/multiply?left=3&right=3")
    assert json.loads(r.data.decode()) == 9


def test_headers(test_app):
    r = test_app.get("/api/v1/header")
    assert r.headers["x-nothing"] == "value"


def test_complex(test_app):
    r = test_app.post(
        "/complex/3",
        data=json.dumps({"body": "1"}),
        headers={"header": "2", "content-type": "application/json"},
    )
    assert json.loads(r.data.decode()) == "1:2:3"


def test_api_exception(test_app):
    r = test_app.get("/exception")
    assert r.status_code == 400
    resp = json.loads(r.data.decode())
    assert resp["code"] == 400
    assert resp["success"] is False


def test_swagger(test_app):
    r = test_app.get("/swagger.json")
    swagger = json.loads(r.data.decode())
    assert swagger["info"] == {"version": "1.0", "title": "example"}
    assert "/multiply" in swagger["paths"]
    assert "/exception" in swagger["paths"]
    # test blueprint is documented as well
    assert "/blueprint/foo" in swagger["paths"]


def test_swagger_html(test_app):
    r = test_app.get("/api/")
    assert "/swagger.json" in r.data.decode()
    assert r.status_code == 200
