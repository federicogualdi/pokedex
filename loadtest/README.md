# Load Testing - Pokédex API (k6)

This directory contains a **load test** for the Pokédex HTTP API, implemented using **k6** (Grafana Labs).

The goal of this test is to validate the performance characteristics of the API at its **HTTP boundary**, in line with a **DDD + Hexagonal Architecture** approach.

---

## Scope

The test focuses on two public read endpoints:

1. `GET /api/pokemon/{name}`
   Returns a Pokémon by name.

2. `GET /api/pokemon/translated/{name}`
   Returns the same Pokémon with a translated description.
   This endpoint is expected to be more expensive due to additional application logic and/or external dependencies.

Both endpoints are exercised concurrently to allow direct comparison under load.

---

## How the test works

### Virtual users and load profile

The test defines two independent k6 scenarios:

- **Plain Pokémon endpoint**
  - Ramps up to 10 concurrent virtual users
- **Translated Pokémon endpoint**
  - Ramps up to 5 concurrent virtual users

Each scenario:
- ramps up gradually
- sustains load for a short period
- ramps down gracefully

This setup reflects a realistic situation where the “core” endpoint is called more frequently than the more expensive translated variant.

---

### Request variability

Each request targets a **random Pokémon name**, selected from a predefined list:

```
pikachu, charizard, mewtwo, bulbasaur, squirtle, eevee
```


This avoids unrealistic hot-spotting on a single path parameter and reduces the impact of trivial caching.

The list can be overridden via environment variables.

---

### Functional checks

Each response is validated with lightweight checks:

- HTTP status code is `200`
- Expected fields are present in the JSON payload

These checks ensure that performance metrics are collected only for *successful and semantically valid* responses.

---

### Performance thresholds

The test enforces explicit performance thresholds:

- Less than 1% failed requests overall
- 95th percentile latency:
  - `< 400ms` for `/api/pokemon/{name}`
  - `< 800ms` for `/api/pokemon/translated/{name}`
  - `< 500ms` globally

If thresholds are violated, the test fails.
This makes the test suitable for use in CI pipelines as a performance regression guard.

---

## Why Docker is used

k6 is executed inside a Docker container to ensure:

- reproducibility across environments
- zero local dependency management
- consistent execution in CI/CD

Important note:
`localhost` inside a container does **not** refer to the host machine.
For this reason, the test targets the API via:

```
http://host.docker.internal
```


The provided Makefile handles this detail transparently.

---

## How to run the test

### Prerequisites

- Docker
- The Pokédex API running locally (default: `http://localhost:8000`)

---

### Recommended command

```bash
make loadtest
```

This is the only command required.
All Docker flags and environment wiring are handled internally.

---

# Configuration

## Base URL

The default target is:

```
http://host.docker.internal:8000
```

You can override it explicitly:

```
make loadtest BASE_URL=http://host.docker.internal:8000
```

---

## Pokémon name list

You can customize the set of Pokémon used during the test:

```
make loadtest POKEMON_NAMES=pikachu,mew,ditto,psyduck
```

---

## Architectural intent

This load test deliberately operates outside the domain layer.

It treats the application as a black box and interacts only through its HTTP interface, exactly like a real client would.
This aligns with hexagonal architecture principles and allows the test to:

- validate adapter-level behavior
- measure the cost of specific use cases
- detect performance regressions independently of implementation details
