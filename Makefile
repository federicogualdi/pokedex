install:
	poetry install --without dev

install-dev:
	poetry install
	poetry run pre-commit install

run:
	poetry run uvicorn --reload --host 0.0.0.0 --port 8000 pokedex.entrypoints.rest.server:app

test:
	poetry run pytest

lint:
	poetry run pre-commit run --all-files
