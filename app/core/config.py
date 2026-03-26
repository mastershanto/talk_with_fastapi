from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "talk_with_fastapi"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./app.db"
    jwt_secret_key: str = "changeme"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    log_level: str = "INFO"
    ml_model_path: str | None = None


settings = AppSettings()
