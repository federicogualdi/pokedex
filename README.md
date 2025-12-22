# Pokedex API


## Installation

Install poetry:

```bash
  curl -sSL https://install.python-poetry.org | python3 -
```

Install project dependencies:

```bash
  make install
```

Install dev dependencies and enable pre-commit hooks:

```bash
  make install-dev
```


## Running the Application

Start the server:

```bash
  make run
```


## Developers

### API Documentation (Swagger / OpenAPI)

When the application is running locally, the interactive API documentation
is available at:

http://localhost:8000/api/docs


Use this interface to:
- explore available endpoints
- inspect request/response schemas
- execute API calls directly from the browser


### Development Commands

Run the test suite:

```bash
  make test
```

Run code linting and static checks:

```bash
  make lint
```

## Documentation

Documentation: [View Docs](DOCS.md)
