from typing import Optional, Any
from pathlib import Path
from pydantic import PostgresDsn, field_validator, ValidationError, Field
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TITLE: str = "Anagram Service"
    DESCRIPTION: str = "API to find similar words"
    API_VERSION: str = 'v1'

    CURRENT_FILE: Path = Path(__file__)
    WORD_MAX_LENGTH: int = 100

    # Database Configuration
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_uri(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if v:
            logger.info("Using provided SQLALCHEMY_DATABASE_URI")
            return v

        username = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        host = info.data.get("POSTGRES_HOST")
        db_name = info.data.get("POSTGRES_DB")

        logger.debug(f"POSTGRES_HOST: {host}, POSTGRES_DB: {db_name}")

        if not username or not username.strip() or not password or not password.strip():
            logger.error("POSTGRES_USER and POSTGRES_PASSWORD must be set and non-empty")
            raise ValueError("POSTGRES_USER and POSTGRES_PASSWORD must be set and non-empty")

        try:
            dsn = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=username,
                password=password,
                host=host,
                path=db_name if db_name else None
            )
            return dsn
        except ValidationError as e:
            raise ValueError(f"Error constructing DSN: {e}") from e

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _ = self.SQLALCHEMY_DATABASE_URI

    class Config:
        """
        Configuration class for environment file settings.

        Attributes:
            env_file (str): Path to the environment file.
            env_file_encoding (str): Encoding of the environment file.
        """
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
