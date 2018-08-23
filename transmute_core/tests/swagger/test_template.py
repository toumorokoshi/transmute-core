from transmute_core.swagger.template import Template


def test_template():
    t = Template("{{foo}}")
    assert t.render(foo="bar") == "bar"
