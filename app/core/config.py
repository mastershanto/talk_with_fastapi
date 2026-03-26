# Global configuration (database, auth, etc.)

from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'fastapi_project'
    debug: bool = True

settings = Settings()
