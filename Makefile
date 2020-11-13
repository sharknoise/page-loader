install:
	poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest

test-coverage:
	poetry run pytest tests --cov=page_loader --cov-report xml


.PHONY: install lint test test-coverage
