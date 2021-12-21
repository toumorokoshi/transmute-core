SWAGGER_UI_VERSION = 3.20.9
TEMP_DIRECTORY = /tmp/transmute_core/

.venv: pyproject.toml
	python -m virtualenv .venv

.venv/deps: .venv pyproject.toml setup.cfg
	.venv/bin/python -m pip install .[test] build pytest twine
	touch .venv/deps

build: .venv/deps
	rm -rf ./dist/
	.venv/bin/python -m build .

upload: build download-deps .venv/deps
	.venv/bin/python -m twine upload dist/*

# only works with python 3+
lint: .venv/deps
	.venv/bin/python -m pip install black==21.12b0
	.venv/bin/python -m black .

lint-check: .venv/deps
	.venv/bin/python -m black --check .

test: .venv/deps
	.venv/bin/python -m pytest transmute_core/ $(ARGS)

ready-pr: test lint

download-deps:
	mkdir -p $(TEMP_DIRECTORY)
	curl -L "https://github.com/swagger-api/swagger-ui/archive/v$(SWAGGER_UI_VERSION).tar.gz" -o $(TEMP_DIRECTORY)/swagger-ui.tar.gz
	tar -xzvf $(TEMP_DIRECTORY)/swagger-ui.tar.gz --strip-components=1 --directory=$(TEMP_DIRECTORY)
	mv $(TEMP_DIRECTORY)/dist/* ./transmute_core/swagger/static/
	rm -r $(TEMP_DIRECTORY)