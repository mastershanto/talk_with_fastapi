from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.modules.ml_model.presentation.routes import router as ml_router
from app.modules.todo.data.models import TodoORM
from app.modules.todo.presentation.routes import router as todo_router

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(todo_router)
app.include_router(ml_router)


@app.on_event("startup")
async def startup_event() -> None:
    async with engine.begin() as conn:
        # Create tables for the todo module
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
