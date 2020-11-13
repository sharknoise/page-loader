install:
	poetry install

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

test-coverage:
	poetry run pytest tests --cov=gendiff --cov-report xml


.PHONY: install lint test test-coverage
