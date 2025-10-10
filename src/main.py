import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.config import settings
from src.exceptions import (
    AppException,
    app_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)
from src.items.router import router as items_router
from src.utils.router import router as utils_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(items_router, prefix="/api/v1")
app.include_router(utils_router, prefix="/api/v1")

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)

# Include private router for local development
if settings.ENVIRONMENT == "local":
    try:
        from src.private.router import router as private_router
        app.include_router(private_router, prefix="/api/v1")
    except ImportError:
        # Private module is optional
        pass
