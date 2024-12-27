from contextvars import ContextVar
from typing import Optional

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

__all__ = ["global_userid", "register_middlewares"]

global_userid: ContextVar[Optional[int]] = ContextVar("global_userid", default=None)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


class BackgroundMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if "background" in request.state._state:
            response.background = request.state.background
        return response


def register_middlewares(app: FastAPI):
    # if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        # allow_origin_regex=settings.CORS_ORIGINS_REGEX,
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    # app.add_middleware(BackgroundMiddleware)
    # app.add_middleware(CorrelationIdMiddleware)

