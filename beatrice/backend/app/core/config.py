"""Application settings."""

import pydantic


class Settings(pydantic.BaseSettings):
    """Contains the application settings."""
    APP_NAME: str = "Beatrice"
    DB_URI: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    ADMIN_USERNAME: str
    ADMIN_EMAIL: str
    ADMIN_NAME: str
    ADMIN_PASSWORD: str

    class Config:
        """Contains Pydantic's configuration."""
        env_file: str = ".env"
        case_sensitive: bool = True


settings = Settings()
