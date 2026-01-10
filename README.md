# Pokedex API

REST API for Pokémon data, built with FastAPI and Python 3.13.

## Live API (Swagger / OpenAPI)

A deployed version of the API is available at:

https://pokedex.federicogualdi.com/api/docs

This page is generated automatically by FastAPI using **Swagger / OpenAPI** and provides:
- interactive documentation of all available endpoints
- request and response schemas
- the ability to execute API calls directly from the browser

The instance available at the URL above is a **live, already deployed version** of the Pokedex API.

Note:
- The hosting provider may stop the container when it is idle.
- If the service was stopped, it can take **up to ~1 minute** after opening the link for the container to start and for the Swagger UI to become available.


---

The project supports:
- local development with Poetry
- containerized development and execution with Docker Compose
- testing, linting, and coverage enforcement
- CI integration via GitHub Actions

---

## Environment Configuration

Copy the sample environment file and adjust values as needed.

```bash
cp .env.sample .env
```

Main configuration options:

- LOG_LEVEL – application log level (DEBUG, INFO, etc.)
- DEBUG – enable or disable debug mode
- PREFERRED_LANGUAGE – default language for Pokémon descriptions
- HTTP_TIMEOUT_SECONDS – timeout for outbound HTTP calls
- REST_EXPOSED_SERVER_PORT – port exposed on the host
- DOCKER_IMAGE_SUFFIX – image tag suffix (dev or prod)

No secrets are required for local development.

---

## Requirements

### General

The project relies on **GNU Make** as the primary command interface.

All supported workflows - local development, Docker Compose operations, testing, linting, and coverage - are exposed via the provided [`Makefile`](Makefile).

---

### Execution Modes

You can run the project in one of the following ways.

#### Option A – Local (Poetry)

Required tools:
- Python 3.13
- Poetry >= 2

This option is recommended if you prefer running the application and tooling directly on your host system.

#### Option B – Containerized (recommended)

Required tools:
- Docker
- Docker Compose (v2 plugin)

This option requires no local Python or Poetry installation and provides the highest parity with CI and production-like environments.

---

### GNU Make

GNU Make is **recommended** and used as the official interface to interact with the project.

All common tasks are wrapped as Make targets:
- application lifecycle (build, run, stop)
- Docker Compose operations
- tests and linting
- coverage generation and enforcement
#### Make is recommended, but not strictly required

If `make` is not installed on your system and cannot be installed, you can still work with the project by executing the underlying commands directly.

All commands executed by Make are plain shell commands and can be inspected in the [`Makefile`](Makefile), which should be treated as the **source of truth** for the exact commands and flags used by the project.

Examples:

- `make test` wraps:
  ```
  poetry run pytest
  ```

- `make coverage` wraps:
  ```
  poetry run coverage run -m pytest
  poetry run coverage report
  poetry run coverage html
  ```

- `make compose-up` wraps:
  ```
  docker compose up -d
  ```

---

## Poetry Local Development (Option A)

### Install Poetry

```
curl -sSL https://install.python-poetry.org | python3 -
```

Verify installation:

```
poetry --version
```

### Install dependencies

Install production dependencies only:

```
make install
```

Install development dependencies and enable pre-commit hooks:

```
make install-dev
```

---

### Running the Application Locally

```
make run
```

The API will be available at:

```
http://localhost:8000
```

---

### Testing and Quality Checks (Local)

#### Run tests

```
make test
```

#### Run linting and static checks

```
make lint
```

#### Generate coverage report

```
make coverage
```

This command:
- runs the test suite
- prints a coverage summary to stdout
- generates XML coverage reports in ./reports
- generates an HTML report in ./htmlcov

#### Enforce coverage threshold

```
make check-coverage-threshold target_coverage=95
```

The command fails if the total coverage percentage is below the specified threshold.

---

## Docker and Docker Compose (Option B)

Docker Compose is the recommended way to run the project without installing Python or Poetry locally.

### Build the image

```
make compose-build
```

### Start the service

```
make compose-up
```

The API will be available at:

```
http://localhost:${REST_EXPOSED_SERVER_PORT}
```

### Stop the service

```
make compose-down
```

### View logs

```
make compose-logs
```

---

### Tests and Coverage with Docker Compose

#### Run tests inside the container

```
make compose-test
```

#### Run coverage inside the container

```
make compose-coverage
```

Notes:
- Coverage runs with DEBUG=0 to avoid interference from debug tooling.
- The HTML coverage report is generated in ./htmlcov on the host.

---

## API Documentation

When the application is running locally, the interactive OpenAPI documentation is available at:

```
http://localhost:8000/api/docs
```

This interface allows you to:
- explore available endpoints
- inspect request and response schemas
- execute API calls directly from the browser

---

## CI Integration

The project is designed to work with GitHub Actions.

Typical CI steps:
- install dependencies with Poetry
- run tests
- generate coverage reports
- enforce a configurable coverage threshold

Example:

```
make coverage
make check-coverage-threshold target_coverage=${COVERAGE_THRESHOLD}
```

---

## Documentation

Documentation: [View Docs](DOCS.md)
