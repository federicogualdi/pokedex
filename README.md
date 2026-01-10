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

You can run the project in two different ways.

### Option A – Local (Poetry)

- Python 3.13
- Poetry >= 2
- GNU Make

### Option B – Containerized (recommended)

- Docker
- Docker Compose (v2 plugin)

No local Python or Poetry installation is required when using Docker.

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
