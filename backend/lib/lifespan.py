from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine

from settings import settings
from database.connection import setup_db_engine
from database.db_utils import initialize_tables, load_word_dataset

from dependencies import get_db_session_app
import logging

logger = logging.getLogger(__name__)


class AppState:
    db_engine: Optional[AsyncEngine] = None
    db_session_factory: Optional[async_sessionmaker] = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Context manager for managing the application lifespan.

    This function initializes resources on startup and cleans up on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    """
    try:
        await _startup_db(app)
        yield
    finally:
        await _shutdown_db(app)


async def _startup_db(app: FastAPI) -> None:
    """
    Perform startup tasks related to the db.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    try:
        await setup_db_engine(app=app)
        await initialize_tables(engine=app.state.db_engine)
        await _load_words_dataset(app=app)
    except Exception as e:
        # todo: logging
        raise


async def _shutdown_db(app: FastAPI) -> None:
    """
    Perform shutdown tasks related to the db.
    Args:
        app: The FastAPI application instance.
    """
    try:
        if app.state.db_engine:
            await app.state.db_engine.dispose()
    except Exception as e:
        print(f"Error during database shutdown: {e}")


async def _load_words_dataset(app: FastAPI) -> None:
    """
    Load the words dataset into the database if the Word table is empty.
    """
    words_dataset_path = settings.CURRENT_FILE.parent / "dataset/words_dataset.txt"

    async with get_db_session_app(app) as db_session:
        await load_word_dataset(dataset_path=words_dataset_path, db_session=db_session)
