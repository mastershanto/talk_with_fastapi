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

  persistence/       ORM models + persistence adapters (SQLAlchemy)
  modules/           Feature modules (ports, services/use cases, routers, schemas)
  routers/           Router shims (stable imports for main.py)

Legacy compatibility
--------------------
`app/repositories/` exists for historical reasons (CRUD-style services) but
new feature work should prefer `app/modules/*` + ports/use-cases.
"""

__version__ = "2.0.0"
