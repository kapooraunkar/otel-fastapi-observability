# ---------------------------------------------------
# CORE APPLICATION SETUP
# ---------------------------------------------------
# This file contains reusable setup functions
# used during FastAPI application startup.
#
# Instead of dumping everything inside main.py,
# we separate:
# - route registration
# - telemetry instrumentation
# - exception handling
#
# This keeps the application architecture cleaner
# and easier to scale later.


from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse


# custom application exceptions
from app.core.exceptions import (
    UserNotFoundException
)


# API routers
from app.api.users import (
    router as user_router
)

from app.api.products import (
    router as product_router
)

from app.api.health import (
    router as health_router
)


# OpenTelemetry instrumentation
from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)

from opentelemetry.instrumentation.requests import (
    RequestsInstrumentor
)


# ---------------------------------------------------
# REGISTER ROUTES
# ---------------------------------------------------
# Centralized router registration.
#
# All API endpoints are connected to the app here.
#
# This becomes useful later when application grows
# and new modules like:
# - payments
# - authentication
# - inventory
# - analytics
# are added.


def register_routes(app: FastAPI):

    app.include_router(user_router)

    app.include_router(product_router)

    app.include_router(health_router)


# ---------------------------------------------------
# SETUP INSTRUMENTATION
# ---------------------------------------------------
# Automatically instruments:
# - FastAPI incoming requests
# - outgoing HTTP requests
#
# This allows observability tools like:
# - OpenTelemetry
# - Niriksha AI
# to automatically collect traces/spans
# without manually tracing every request.


def setup_instrumentation(app: FastAPI):

    # traces incoming FastAPI requests
    FastAPIInstrumentor.instrument_app(app)

    # traces outgoing HTTP requests
    RequestsInstrumentor().instrument()


# ---------------------------------------------------
# EXCEPTION HANDLERS
# ---------------------------------------------------
# Converts application exceptions into
# structured API responses.
#
# Instead of crashing application or returning
# ugly errors, we return controlled JSON responses.


def setup_exception_handlers(app: FastAPI):

    @app.exception_handler(
        UserNotFoundException
    )

    async def user_not_found_handler(

        request: Request,

        exc: UserNotFoundException

    ):

        return JSONResponse(

            status_code=404,

            content={

                "error": exc.message

            }
        )