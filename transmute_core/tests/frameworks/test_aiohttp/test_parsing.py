import pytest


@pytest.mark.asyncio
async def test_parsing_multiiple_query_params(cli):
    resp = await cli.get('/multiple_query_params?tag=foo&tag=bar')
    ret_value = await resp.json()
    assert 200 == resp.status
    assert ret_value == "foo,bar"


@pytest.mark.asyncio
async def test_parsing_multiple_query_params_single_tag(cli):
    resp = await cli.get('/multiple_query_params?tag=foo')
    ret_value = await resp.json()
    assert 200 == resp.status
    assert ret_value == "foo"
