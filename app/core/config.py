from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'fastapi_project'
    version: str = '1.0.0'
    debug: bool = True
    sqlalchemy_database_url: str = 'sqlite:///./test.db'
    jwt_secret_key: str = 'CHANGE_ME'
    jwt_algorithm: str = 'HS256'
    jwt_access_token_expires_minutes: int = 60
    backend_cors_origins: list[str] = ['*']

    class Config:
        env_file = '.env'

settings = Settings()
