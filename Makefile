POETRY ?= poetry

name = pyflipt

_default: test

clean:
	find . -name '__pycache__' | xargs rm -rf
	find . -type f -name "*.pyc" -delete

install-dev:
	$(POETRY) install

install:
	$(POETRY) install  --no-dev

format:
	$(POETRY) run isort $(name) tests
	$(POETRY) run black $(name) tests

lint:
	$(POETRY) run isort --check-only $(name) tests
	$(POETRY) run black --check $(name) tests
	$(POETRY) run flake8 --config setup.cfg $(name) tests

mypy:
	$(POETRY) run mypy -p $(name) && $(POETRY) run mypy -p tests

test:
	$(POETRY) run pytest tests

coverage: install-dev
	$(POETRY) run pytest tests --cov=$(name)

version:
	$(POETRY) version $(version)

release:
	# can only support wheels here
	$(POETRY) build -f wheel
	$(POETRY) run twine upload dist/*

.PHONY: clean install install-dev test
