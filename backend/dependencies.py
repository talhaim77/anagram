from fastapi import Request, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db_session(request: Optional[Request] = None,
                         app: Optional[FastAPI] = None
                         ) -> AsyncSession:
    """
    This function yields an asynchronous db session. It determines the session
    factory from either the FastAPI request object or the application instance.

    Args:
        request (Optional[Request]): FastAPI request object (for HTTP contexts).
        app (Optional[FastAPI]): FastAPI application instance (for non-HTTP contexts).

    Returns:
        AsyncSession: An instance of the SQLAlchemy asynchronous session.

    Raises:
        ValueError: If neither `request` nor `app` is provided.
    """
    if request:
        session_factory = request.app.state.db_session_factory
    elif app:
        session_factory = app.state.db_session_factory
    else:
        raise ValueError("At least one of request and app must be provided.")

    session: AsyncSession = session_factory()

    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
