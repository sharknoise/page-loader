install:
	poetry install

lint:
	poetry run flake8 page_load

test:
	poetry run pytest

test-coverage:
	poetry run pytest tests --cov=page_load --cov-report xml


.PHONY: install lint test test-coverage
