import pytest
import json


@pytest.mark.asyncio
async def test_content_type_in_response(cli):
    """the content type should be specified in the response."""
    resp = await cli.get("/optional")
    assert 200 == resp.status
    assert resp.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_headers(cli):
    """the content type should be specified in the response."""
    resp = await cli.get("/headers/")
    assert "boo" == resp.headers["location"]


@pytest.mark.asyncio
async def test_multiply(cli):
    resp = await cli.get("/multiply?left=5&right=10")
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == 50


@pytest.mark.asyncio
async def test_multiply_bad_int(cli):
    resp = await cli.get("/multiply?left=foo&right=0x00")
    assert 400 == resp.status


@pytest.mark.asyncio
async def test_error(cli):
    """HTTPProcessingErrors should be honored."""
    resp = await cli.get("/aiohttp_error")
    assert 403 == resp.status
    text = await resp.text()
    assert "unauthorized" in json.loads(text)["result"]


@pytest.mark.asyncio
async def test_api_exception(cli):
    """APIException should be honored."""
    resp = await cli.get("/api_exception")
    assert 400 == resp.status
    text = await resp.text()
    assert "nope" in json.loads(text)["result"]


@pytest.mark.asyncio
async def test_optional(cli):
    resp = await cli.get("/optional")
    assert 200 == resp.status
    ret_value = await resp.json()
    assert ret_value is False


@pytest.mark.asyncio
async def test_optional_with_value(cli):
    resp = await cli.get("/optional?include_foo=true")
    assert 200 == resp.status
    ret_value = await resp.json()
    assert ret_value is True


@pytest.mark.asyncio
async def test_body_and_header(cli):
    resp = await cli.post(
        "/body_and_header",
        data=json.dumps({"body": "body"}),
        headers={"content-type": "application/json", "header": "header"},
    )
    assert 200 == resp.status
    ret_value = await resp.json()
    assert ret_value is False


@pytest.mark.asyncio
async def test_get_id(cli):
    resp = await cli.get("/id/10")
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == "your id is: 10"


@pytest.mark.asyncio
async def test_config(cli):
    resp = await cli.get("/config")
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == {"test": "foo"}


@pytest.mark.asyncio
async def test_swagger(cli):
    resp = await cli.get("/swagger.json")
    assert 200 == resp.status
    assert "application/json" == resp.headers["Content-Type"]
    text = await resp.text()
    assert json.loads(text)["paths"]["/multiply"]["get"]["responses"] == {
        "200": {"schema": {"type": "integer"}, "description": "success"},
        "400": {
            "schema": {
                "title": "FailureObject",
                "type": "object",
                "required": ["success", "result"],
                "properties": {
                    "result": {"type": "string"},
                    "success": {"type": "boolean"},
                },
            },
            "description": "invalid input received",
        },
    }


@pytest.mark.asyncio
async def test_swagger_page(cli):
    resp = await cli.get("/swagger")
    assert 200 == resp.status
    assert "text/html" == resp.headers["Content-Type"]
