from settings import settings
from sqlalchemy.ext.asyncio import  (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI
from sqlalchemy.orm import DeclarativeBase
import logging

logger = logging.getLogger(__name__)

# Define Base for models
class Base(DeclarativeBase):
    pass


async def setup_db_engine(app: FastAPI) -> None:
    """
    Set up the database engine and session factory.

    This function configures the SQLAlchemy asynchronous engine and session factory
    and stores them in the application state.
    """
    from sqlalchemy.sql import text

    engine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        pool_size=5,  # Max 5 connections per worker
        max_overflow=10,
        echo=False,
    )

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        async with engine.connect() as conn:
            logger.info("Testing database connection...")
            await conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise

    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def get_connection():
    """
    Returns a new database connection using credentials from environment variables.
    """
    import psycopg2
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    try:
        yield conn
    finally:
        conn.close()

