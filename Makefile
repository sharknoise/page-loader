install:
	poetry install

lint:
	poetry run flake8 page_load

test:
	poetry run pytest -o log_cli=True -o log_cli_level=10 --cov=page_load --cov-report=term-missing


.PHONY: install lint test
