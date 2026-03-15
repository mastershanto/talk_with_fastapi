#!/usr/bin/env python
"""Scaffold a new feature-first Clean Architecture module.

Goal
----
Create a minimal, consistent module skeleton that follows:
- Entities (core domain rules)
- Use Cases (application orchestration)
- Interface Adapters (HTTP controller + DTO/presenter)
- Frameworks & Drivers (SQLAlchemy adapter)

This intentionally generates boring, repeatable boilerplate so you can move fast
without re-inventing structure each project.

Usage
-----
  python scripts/scaffold_feature.py favorites

Notes
-----
- This script creates files; it does NOT auto-wire the router into `main.py`.
  That wiring varies per project and should be a deliberate review step.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def _snake(name: str) -> str:
    name = name.strip()
    if not name:
        raise SystemExit("Feature name is required")

    # Accept: `foo_bar`, `FooBar`, `foo-bar`
    name = name.replace("-", "_")
    # camelCase / PascalCase -> snake
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"__+", "_", name)
    name = name.lower()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise SystemExit("Feature name must be alnum/underscore and start with a letter")
    return name


def _title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("_"))


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a Clean Architecture feature module")
    parser.add_argument("name", help="Feature name (snake_case, kebab-case, or PascalCase)")
    args = parser.parse_args()

    feature = _snake(args.name)
    feature_title = _title(feature)

    repo_root = Path(__file__).resolve().parents[1]
    app_dir = repo_root / "app"

    domain_dir = app_dir / "domains" / feature
    infra_file = app_dir / "infrastructure" / "sqlalchemy" / f"{feature}.py"
    router_shim = app_dir / "routers" / f"{feature}.py"

    _write(domain_dir / "__init__.py", f'"""{feature_title} domain."""\n')

    _write(
        domain_dir / "entities.py",
        (
            '"""Entities (core domain model + rules)."""\n\n'
            "from __future__ import annotations\n\n"
            "# Keep this file pure: no FastAPI/SQLAlchemy imports.\n"
        ),
    )

    _write(
        domain_dir / "ports.py",
        (
            '"""Ports (interfaces) for this domain."""\n\n'
            "from __future__ import annotations\n\n"
            "from typing import Protocol\n\n\n"
            f"class {feature_title.replace(' ', '')}Repository(Protocol):\n"
            "    ...\n"
        ),
    )

    _write(
        domain_dir / "use_cases.py",
        (
            '"""Use Cases (application services/orchestration)."""\n\n'
            "from __future__ import annotations\n\n"
            f"class {feature_title.replace(' ', '')}UseCases:\n"
            "    def __init__(self, *, repo) -> None:\n"
            "        self._repo = repo\n"
        ),
    )

    _write(
        domain_dir / "schemas.py",
        (
            '"""Interface adapters: DTOs/presenters for this domain."""\n\n'
            "from __future__ import annotations\n\n"
            "from pydantic import BaseModel\n\n\n"
            f"class {feature_title.replace(' ', '')}Response(BaseModel):\n"
            "    ...\n"
        ),
    )

    _write(
        domain_dir / "router.py",
        (
            '"""Interface adapters: HTTP controller (FastAPI router)."""\n\n'
            "from __future__ import annotations\n\n"
            "from fastapi import APIRouter\n\n\n"
            f"router = APIRouter(prefix='/{feature}', tags=['{feature_title}'])\n"
        ),
    )

    _write(
        infra_file,
        (
            '"""Frameworks & Drivers: SQLAlchemy adapter for this domain."""\n\n'
            "from __future__ import annotations\n\n"
            "from sqlalchemy.orm import Session\n\n\n"
            f"class SqlAlchemy{feature_title.replace(' ', '')}Repository:\n"
            "    def __init__(self, db: Session) -> None:\n"
            "        self._db = db\n"
        ),
    )

    _write(
        router_shim,
        (
            '"""Compatibility shim.\n\n'
            "The project is moving to a feature-first modular monolith. The real router now\n"
            f"lives at `app.domains.{feature}.router`.\n"
            '"""\n\n'
            f"from app.domains.{feature}.router import router\n\n"
            "__all__ = ['router']\n"
        ),
    )

    print("Created:")
    print(f"- {domain_dir.relative_to(repo_root)}")
    print(f"- {infra_file.relative_to(repo_root)}")
    print(f"- {router_shim.relative_to(repo_root)}")
    print("\nNext manual steps:")
    print("- Add DI providers in app/dependencies.py")
    print("- Export shim in app/routers/__init__.py")
    print("- Include router in app/main.py")


if __name__ == "__main__":
    main()
