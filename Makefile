.PHONY:

init:
	@pip install poetry
	@poetry install

t:
	@poetry run python -m unittest tests

t-app:
	@poetry run python -m unittest tests.test_app${T}

example:
	@poetry run python example.py

mypy:
	@poetry run mypy tomoyo/*.py

lint:
	@poetry run black tomoyo/*.py

check: lint mypy
