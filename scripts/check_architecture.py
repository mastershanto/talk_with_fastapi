"""Architecture guard checks.

Fail CI/pre-commit if new Python modules are added under app/repositories.
The domain-first architecture uses app/domains + app/infrastructure as the
primary extension points; app/repositories is legacy compatibility.
"""

from __future__ import annotations

from pathlib import Path


ALLOWED_REPOSITORY_FILES = {
    "__init__.py",
    "base.py",
    "auth.py",
    "property.py",
    "user.py",
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
