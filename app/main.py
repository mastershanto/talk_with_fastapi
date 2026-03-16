"""FastAPI app with all logic consolidated."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.telemetry import init_telemetry
from app.zmain.database import DatabaseInitializer
from app.zmain.lifespan import LifespanManager
from app.zmain.registrars import RouterRegistrar, AdminRegistrar, HealthRegistrar
from app.core.database import SessionLocal

class _Factory:
    def __init__(self) -> None:
        self.db = DatabaseInitializer(SessionLocal)
        self.ls = LifespanManager(self.db)
        self.rr, self.ar, self.hr = RouterRegistrar(), AdminRegistrar(), HealthRegistrar()
    def build(self) -> FastAPI:
        app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=self.ls.lifespan)
        init_telemetry(app)
        app.add_middleware(CORSMiddleware, allow_origins=settings.ALLOWED_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
        register_exception_handlers(app)
        self.rr.register(app)
        self.ar.register(app)
        self.hr.register(app)
        return app

app: FastAPI = _Factory().build()



