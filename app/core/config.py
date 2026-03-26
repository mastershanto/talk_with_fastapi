from pydantic_settings import BaseSettings # pyright: ignore[reportMissingImports]

class Settings(BaseSettings):
    app_name: str = 'fastapi_project'
    version: str = '1.0.0'
    debug: bool = True
    sqlalchemy_database_url: str = 'postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db'
    jwt_secret_key: str = 'CHANGE_ME'
    jwt_algorithm: str = 'HS256'
    jwt_access_token_expires_minutes: int = 60
    backend_cors_origins: list[str] = ['*']

    model_config = {
        'env_file': '.env',
    }

settings = Settings()
