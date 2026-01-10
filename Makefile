# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

############################################## docker compose related targets ##############################################
all: compose-down compose-build compose-up

compose-build:
	docker compose build

compose-up:
	docker compose up -d

compose-down:
	docker compose down --remove-orphans

compose-test:
	docker compose run --rm --no-deps --entrypoint=pytest rest_server

compose-logs:
	docker compose logs -f

compose-destroy:
	docker compose down -v --remove-orphans

compose-ps:
	docker compose ps

# set DEBUG=0 to prevent issues with coverage tool showing wrong percentage due to conflicts with debugpy (just importing it breaks coverage tests collection)
compose-coverage:
	docker compose run --rm --no-deps -e DEBUG=0 --entrypoint= rest_server sh -c "coverage run -m pytest && coverage report && coverage html"


####

coverage:
	poetry run coverage run -m pytest --verbose --junit-xml ./reports/tests.xml
	poetry run coverage report
	poetry run coverage xml -o ./reports/coverage.xml

# check target coverage against threshold
# must be run after running coverage
check-coverage-threshold:
	@if [ -n "$(target_coverage)" ]; then \
		COV_PERCENT=$$(poetry run coverage report | grep -Po "(?<=TOTAL\s).+?(\d+)%" | grep -Po "\d+(?=%)"); \
		echo "Coverage percentage: $$COV_PERCENT%"; \
		if [ "$$COV_PERCENT" -lt "$(target_coverage)" ]; then \
			echo "Error: Coverage threshold not met. Target: $(target_coverage)%, Actual: $$COV_PERCENT%"; \
			exit 1; \
		fi \
	else \
		echo "Error: Coverage threshold not set."; \
		exit 1; \
	fi

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
