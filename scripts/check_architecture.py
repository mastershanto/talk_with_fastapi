"""Architecture guard checks.

Fail CI/pre-commit if new Python modules are added under app/repositories.
The domain-first architecture uses app/domains + app/infrastructure as the
primary extension points; app/repositories is legacy compatibility.
"""

from __future__ import annotations

from pathlib import Path
import re


ALLOWED_REPOSITORY_FILES = {
    "__init__.py",
    "base.py",
    "auth.py",
    "property.py",
    "user.py",
}

ALLOWED_IMPORTERS = {
    "app/repositories/__init__.py",
    "app/repositories/base.py",
    "app/repositories/auth.py",
    "app/repositories/property.py",
    "app/repositories/user.py",
}


def main() -> int:
    repo_dir = Path("app/repositories")
    if not repo_dir.exists():
        return 0

    violations: list[str] = []
    for file in sorted(repo_dir.glob("*.py")):
        if file.name not in ALLOWED_REPOSITORY_FILES:
            violations.append(str(file))

    if violations:
        print("Architecture guard failed.")
        print("New modules under app/repositories are not allowed.")
        print("Use app/domains/<feature>/ + app/infrastructure/sqlalchemy instead.")
        for item in violations:
            print(f" - {item}")
        return 1

    importer_violations: list[str] = []
    import_pattern = re.compile(r"\b(from|import)\s+app\.repositories\b")

    for file in sorted(Path("app").rglob("*.py")):
        rel = file.as_posix()
        if rel in ALLOWED_IMPORTERS:
            continue

        content = file.read_text(encoding="utf-8")
        if import_pattern.search(content):
            importer_violations.append(rel)

    if importer_violations:
        print("Architecture guard failed.")
        print("Importing app.repositories is deprecated outside compatibility files.")
        print("Use app/domains/* ports and app/infrastructure/sqlalchemy adapters instead.")
        for item in importer_violations:
            print(f" - {item}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
