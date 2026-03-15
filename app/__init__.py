"""FastAPI reference project — app package.

This package is organized as a **feature-first modular monolith**.

Core structure
--------------
app/
  config.py          Settings (pydantic-settings, env / .env override)
  database.py        Engine, SessionLocal, Base
  dependencies.py    DI providers (db, services, repos)
  exceptions.py      Custom exceptions + exception handlers
  main.py            Application factory (create_app) + lifespan
  version.py         API versioning constants
  telemetry.py       Structured logging + OpenTelemetry tracing
  secrets.py         Optional external secret loader (Vault)

  models/            SQLAlchemy ORM models
  domains/           Feature modules (ports, use cases, routers, schemas)
  infrastructure/    Adapters (SQLAlchemy implementations of ports)
  routers/           Router shims (stable imports for main.py)
  schemas/           Shared Pydantic schemas

Legacy compatibility
--------------------
`app/repositories/` exists for historical reasons (CRUD-style services) but
new feature work should prefer `app/domains/*` + ports/use-cases.
"""

__version__ = "2.0.0"
