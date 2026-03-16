"""Minimal FastAPI entrypoint.

This module exists so `uvicorn app.main:app` continues to work while all
construction and wiring logic lives in `app.zmain`.
"""

from app.zmain import create_app


app = create_app()
