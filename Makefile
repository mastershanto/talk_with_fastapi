.PHONY: help install-dev format lint typecheck test ci db-upgrade db-revision

help:
	@echo "Targets:"
	@echo "  install-dev  Install dev dependencies"
	@echo "  format       Format (ruff)"
	@echo "  lint         Lint (ruff)"
	@echo "  typecheck    Type check (mypy)"
	@echo "  test         Run tests (pytest)"
	@echo "  ci           Run lint + typecheck + tests"
	@echo "  db-upgrade   Run Alembic migrations (upgrade head)"
	@echo "  db-revision  Create new migration (autogenerate)"

install-dev:
	python -m pip install -U pip
	python -m pip install -r requirements-dev.txt

format:
	python -m ruff format .

lint:
	python -m ruff check .

typecheck:
	python -m mypy app

test:
	pytest

ci: lint typecheck test

db-upgrade:
	python -m alembic upgrade head

db-revision:
	python -m alembic revision --autogenerate -m "change"
