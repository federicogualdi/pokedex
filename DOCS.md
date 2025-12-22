# Pokedex API – Architecture & Design Documentation

## Overview

This project is a **FastAPI-based backend service** that exposes Pokémon information retrieved from external providers.

The primary goal of the project is not only to deliver a working API, but to demonstrate:
- **Domain-Driven Design (DDD)**
- **Hexagonal (Ports & Adapters) Architecture**
- A clean separation of concerns
- A strong and structured **testing strategy**
- Incremental and production-oriented development

The project is intentionally structured to remain **maintainable, testable, and extensible** as new features are added.

---

## High-level Architecture

The application follows a **Hexagonal Architecture** approach:

- The **Domain** is at the center and contains business logic and rules
- **Ports** define what the domain needs
- **Adapters** implement those ports to integrate with external systems
- **Entry points** expose the domain via HTTP (REST)

```
┌────────────────────────────┐
│ Entry Points               │
│ (FastAPI, REST API)        │
└─────────────┬──────────────┘
              │
┌─────────────▼──────────────┐
│ Domain                     │
│ (Models, Services,         │
│ Ports, Errors)             │
└─────────────┬──────────────┘
              │
┌─────────────▼──────────────┐
│ Infrastructure             │
│ (HTTP clients, adapters,   │
│ third-party providers)     │
└────────────────────────────┘
```

---

## Domain-Driven Design

### Domain Model

The Pokémon domain is intentionally simple and explicit.

#### Model

```python
class Pokemon(BaseModel):
    name: str
    description: str
    habitat: str | None
    is_legendary: bool = Field(alias="isLegendary")
```

The domain model:
- Is independent from HTTP and FastAPI
- Uses Pydantic for validation and serialization
- Represents the core business concept without transport concerns

---

## Domain Errors

Errors are modeled as semantic domain exceptions, not HTTP exceptions.

```python
class PokemonNotFoundError(NotFoundError):
    def __init__(self, pokemon_name: str):
        super().__init__(f"Pokemon '{pokemon_name}' not found")
        self.pokemon_name = pokemon_name
```

Key principles:
- Errors describe what went wrong, not how it is exposed
- No HTTP status codes in the domain
- Errors can be reused across different entry points

---

## Domain Port

The domain defines what it needs, not how it is implemented.

```python
class PokemonSpeciesPort(Protocol):
    async def get_species_info(self, name: str) -> Pokemon:
        ...
```

This port represents a dependency on a Pokémon species information provider.
The domain does not care whether the data comes from:

- A REST API
- A database
- A cache
- A mock or fake implementation

---

## Domain Service

The domain service is responsible for orchestrating domain operations by delegating data access to ports.

```python
class PokemonService:
    def __init__(self, species_port: PokemonSpeciesPort):
        self._species_port = species_port

    async def get_pokemon(self, name: str) -> Pokemon:
        return await self._species_port.get_species_info(name)
```

Responsibilities:

- Orchestrates domain operations
- Delegates data access to ports
- Contains no infrastructure or HTTP logic

---

## Hexagonal Architecture (Ports & Adapters)

### Adapters

Adapters live in the infrastructure layer and implement domain ports.

Example responsibilities of an adapter:

- Perform HTTP requests to third-party APIs
- Handle timeouts and network errors
- Map external DTOs to domain models
- Translate external failures into domain errors

Adapters depend on the domain.
The domain never depends on adapters.

---

## Entry Points (REST API)

The REST layer is implemented using FastAPI and is responsible for:

- Request validation
- Response serialization
- Dependency injection
- Error mapping

Key rules:

- No business logic in routes
- No HTTP-specific code in the domain
- Domain errors are translated into HTTP responses via exception handlers

---

## Configuration Management

All configuration is managed via Pydantic Settings and environment variables.

Characteristics:

- Strong typing
- Validation at startup
- Environment-driven behavior

This allows the application to be configured without code changes across environments.

---

## Error Handling Strategy

The project uses a layered error handling approach:

### Domain layer
- Raises semantic errors (e.g. PokemonNotFoundError)

### Infrastructure layer
- Translates third-party failures into domain errors

### Entry points
- Map domain errors to HTTP responses

This keeps the domain:

- Transport-agnostic
- Reusable
- Easy to test

---

## Testing Strategy

The project follows a testing pyramid.

### Unit Tests
- Test domain services and models in isolation
- Use fakes or mocks for ports
- No FastAPI, no HTTP

### Integration Tests
- Test REST endpoints
- Verify dependency wiring
- Mock external providers
- Validate request/response schemas and error mapping

### End-to-End Tests
- Smoke tests covering the full application stack
- Deterministic (no real external calls)
- Validate system behavior from HTTP request to response

This strategy provides fast feedback and high confidence without flaky tests.

---

## Incremental Development Approach

The project is built incrementally using small, vertical slices.

Each iteration:

- Delivers a working feature
- Is fully test-covered
- Can be safely extended

### Examples of iterations:

#### Core Pokémon retrieval (Issue #3)
Establishes the minimum viable product by introducing the Pokémon domain model, the core domain service, and the first port for species retrieval. This iteration defines the foundational boundaries of the system and validates the Domain-Driven Design approach.

#### First translation feature – Shakespeare only (Issue #4)
Introduces the first translation capability as an external concern, validating the Hexagonal Architecture by integrating a third-party provider without modifying the core Pokémon retrieval logic.

#### Business rule for translation strategy (Issue #5)
Moves decision-making logic into the domain by defining explicit business rules for selecting the translation strategy. This iteration removes conditional logic from entry points and makes the behavior explicit and testable.

#### Second translation feature – Yoda (Issue #6)
Extends the system by adding a new translation provider that implements the same domain port. No changes are required to existing domain services, demonstrating extensibility and adherence to the open/closed principle.

#### Performance optimization via caching (Issue #7)
Introduces a local cache at the infrastructure level to improve performance and reduce calls to third-party services. The cache is completely transparent to the domain and does not alter business logic.

#### Resilience and retries (Issue #8)
Strengthens system robustness by introducing retry policies and resilience mechanisms for third-party interactions. These concerns remain confined to the infrastructure layer, preserving the purity of the domain.

This incremental approach ensures that the architecture evolves deliberately, with each step reinforcing the separation of concerns and the overall design principles.

---

## Design Principles

The codebase follows these principles:

- Single Responsibility Principle
- Dependency Inversion
- Explicit dependencies
- Separation of concerns
- Testability first

---

## Summary

This project demonstrates how to build a clean backend service by combining:

- Domain-Driven Design
- Hexagonal Architecture
- FastAPI best practices
- Strong testing discipline

The result is a codebase that is easy to reason about, easy to test, and ready to evolve.
