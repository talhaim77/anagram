import os
import pytest
from unittest.mock import patch, MagicMock
from backend.settings import Settings  # Adjust the import path based on your project structure


def test_sqlalchemy_database_uri_valid():
    """
    Test that the SQLALCHEMY_DATABASE_URI is assembled correctly when environment variables are set.
    """
    os.environ["POSTGRES_USER"] = "postgres"
    os.environ["POSTGRES_PASSWORD"] = "root971"
    os.environ["POSTGRES_HOST"] = "db:5432"
    os.environ["POSTGRES_DB"] = "anagram_db"

    try:
        settings = Settings()
        expected_uri = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
        assert str(settings.SQLALCHEMY_DATABASE_URI) == expected_uri
    finally:
        os.environ.pop("POSTGRES_USER", None)
        os.environ.pop("POSTGRES_PASSWORD", None)
        os.environ.pop("POSTGRES_HOST", None)
        os.environ.pop("POSTGRES_DB", None)


def test_sqlalchemy_database_uri_provided():
    """
    Test that the provided SQLALCHEMY_DATABASE_URI is used when explicitly set.
    """
    os.environ["SQLALCHEMY_DATABASE_URI"] = "postgresql+asyncpg://explicit_user:explicit_password@explicit_host/explicit_db"
    settings = Settings()
    expected_uri = "postgresql+asyncpg://explicit_user:explicit_password@explicit_host/explicit_db"
    assert str(settings.SQLALCHEMY_DATABASE_URI) == expected_uri
    os.environ.pop("SQLALCHEMY_DATABASE_URI", None)
