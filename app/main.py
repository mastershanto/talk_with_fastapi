from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]

from app.core.config import settings
from app.modules.todo_module.presentation.routes import router as todo_router
from app.modules.auth_module.presentation.routes import router as auth_router
from app.modules.ai_module.presentation.routes import router as ai_router

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    description='Enterprise-grade FastAPI Clean Architecture example',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router, prefix='/auth', tags=['Authentication'])
app.include_router(todo_router, prefix='/todos', tags=['Todo'])
app.include_router(ai_router, prefix='/ai', tags=['AI'])

@app.get('/')
def root():
    return {'status': 'up', 'app': settings.app_name}
