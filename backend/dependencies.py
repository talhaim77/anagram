from fastapi import Request, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from contextlib import asynccontextmanager


# backend/dependencies.py

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session using the Request object.

    Args:
        request (Request): FastAPI request object.

    Yields:
        AsyncSession: An instance of the SQLAlchemy asynchronous session.
    """
    session_factory = request.app.state.db_session_factory
    session: AsyncSession = session_factory()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


@asynccontextmanager
async def get_db_session_app(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session using the FastAPI application instance.

    Args:
        app (FastAPI): FastAPI application instance.

    Yields:
        AsyncSession: An instance of the SQLAlchemy asynchronous session.
    """
    session_factory = app.state.db_session_factory
    session: AsyncSession = session_factory()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()