from __future__ import annotations

import os
import tempfile
from pathlib import Path


# Ensure tests are hermetic by default:
# - Use SQLite file DB (fast, zero external deps)
# - Keep it in a temp dir to avoid polluting the repo
_tmp_dir = Path(tempfile.mkdtemp(prefix="talk_with_fastapi_tests_"))
_db_path = _tmp_dir / "test.db"

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{_db_path.as_posix()}")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
