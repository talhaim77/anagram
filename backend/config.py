from typing import Optional, Any
from pathlib import Path
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TITLE: str = "Anagram Service"
    DESCRIPTION: str = "API to find similar words"
    API_VERSION: str = 'v1'

    CURRENT_FILE: Path = Path(__file__)

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_NAME: str = "anagram_db"
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_uri(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("DB_HOST"),
            path=f"/{info.data.get('DB_NAME')}"
        )

    class Config:
        """
        Configuration class for environment file settings.

        Attributes:
            env_file (str): Path to the environment file.
            env_file_encoding (str): Encoding of the environment file.
        """
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Config()
