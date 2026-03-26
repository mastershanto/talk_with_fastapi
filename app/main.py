import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pythonjsonlogger.json import JsonFormatter  # type: ignore[attr-defined]  # pyright: ignore [reportMissingImports]

from app.core.config import settings
from app.core.database import Base, engine
from app.modules.auth.presentation.routes import router as auth_router
from app.modules.ml_model.presentation.routes import router as ml_router
from app.modules.todo.presentation.routes import router as todo_router


def configure_logging() -> None:
    formatter = JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(settings.log_level)
    if not root.hasHandlers():
        root.addHandler(handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logging.getLogger(__name__).info("Application startup")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logging.getLogger(__name__).info("Application shutdown")


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(todo_router, prefix="/api/v1")
app.include_router(ml_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health() -> dict:
    return {"status": "ok"}
