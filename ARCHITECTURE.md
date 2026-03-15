# Real Estate Enterprise API — Architecture

This repository is intended to be a **reusable FastAPI boilerplate** you can copy into future projects.

Design goals:

- **Feature-first modular monolith**: add features without reorganizing the whole app.
- **Clean Architecture (Uncle Bob) / Hexagonal**: dependencies point inward; infrastructure is pluggable.
- **Rapid development**: predictable structure + DI + scaffolding.
- **Long-lived maintainability**: explicit boundaries, boring patterns, minimal magic.

## Folder structure (high level)

```text
app/
  domains/                 # Use-case-centric feature modules
    auth/                  # registration/login/OTP/password reset/profile
    users/                 # users CRUD
    properties/            # properties CRUD
    favorites/             # property favorites

  infrastructure/          # concrete adapters (DB/external services)
    sqlalchemy/            # SQLAlchemy implementations of ports

  models/                  # ORM models (DB schema)
  schemas/                 # Pydantic request/response schemas
  routers/                 # compatibility shims (re-export domain routers)

  dependencies.py          # DI wiring (ports -> adapters -> use-cases)
  main.py                  # app factory + router registration + lifespan
  exceptions.py            # consistent error handling
  response_formatter.py    # response envelope helpers
  security.py              # JWT auth dependency (CurrentUser)
```

## Clean Architecture layers (in this repo)

For a given feature `X`:

### 1) Entities (core domain model + rules)

- Location: `app/domains/X/entities.py`
- Must NOT import FastAPI/SQLAlchemy.
- Holds domain types and pure business rules.

Example: `app/domains/favorites/entities.py` defines `Favorite`.

### 2) Use Cases (application services/orchestration)

- Location: `app/domains/X/use_cases.py` (or `service.py` in existing modules)
- Coordinates domain logic.
- Depends only on:
  - Entities
  - Ports (interfaces)
  - Application exceptions

Example: `app/domains/favorites/use_cases.py`.

### 3) Interface Adapters (controllers/presenters/gateways)

- Location: `app/domains/X/router.py` and `app/domains/X/schemas.py`
- Implements HTTP endpoints and request/response mapping.
- Calls use-cases.

Example: `app/domains/favorites/router.py`.

### 4) Frameworks & Drivers (FastAPI / DB / external services)

- Location: `app/infrastructure/sqlalchemy/*.py` and `app/models/*.py`
- Implements the ports (interfaces) using SQLAlchemy.

Example: `app/infrastructure/sqlalchemy/favorites.py` + `app/models/favorite.py`.

## Dependency rule (the “future-proof” core)

**Allowed dependencies** (outer -> inner):

- Interface Adapters can depend on Use Cases, Entities, Ports.
- Use Cases can depend on Entities and Ports.
- Infrastructure depends on Ports and Frameworks.

**Not allowed**:

- Use Cases importing FastAPI or SQLAlchemy.
- Entities importing anything outside the domain.

## FastAPI wiring strategy

- `app/main.py` includes routers under `/api/v1`.
- `app/routers/*.py` are **compatibility shims** that re-export `router` from the feature module.
  This keeps the app wiring stable as modules evolve.

## Response envelope

Success responses follow:

```json
{
  "success": true,
  "message": "...",
  "data": {"...": "..."},
  "code": 200
}
```

Helpers live in `app/response_formatter.py`.

## Adding a new feature quickly

1. Scaffold the module:

```bash
python scripts/scaffold_feature.py my_feature
```

1. Implement:

- `entities.py` (pure domain)
- `ports.py` (interfaces)
- `use_cases.py` (orchestration)
- `router.py` + `schemas.py` (HTTP adapter)
- `infrastructure/sqlalchemy/my_feature.py` (DB adapter)

1. Wire it:

- Add DI providers in `app/dependencies.py`
- Export shim in `app/routers/__init__.py`
- Include router in `app/main.py`

## Testing philosophy

The `tests/` suite defaults to **SQLite file DB** (no external Postgres requirement).

- `tests/conftest.py` sets `DATABASE_URL` before the app imports.
- Use `with TestClient(app) as client:` so FastAPI lifespan runs and creates tables.

Run:

```bash
pytest
```
