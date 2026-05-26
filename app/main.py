from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)

from opentelemetry.instrumentation.requests import (
    RequestsInstrumentor
)


# initializes OTEL tracing
from app.telemetry.tracing import tracer


# routers
from app.routers.users import (
    router as user_router
)

from app.routers.products import (
    router as product_router
)

from app.routers.health import (
    router as health_router
)


# -----------------------------
# FASTAPI APP
# -----------------------------

app = FastAPI()


# -----------------------------
# OTEL INSTRUMENTATION
# -----------------------------

# automatically traces FastAPI requests
FastAPIInstrumentor.instrument_app(app)

# traces outgoing HTTP requests
RequestsInstrumentor().instrument()


# -----------------------------
# REGISTER ROUTERS
# -----------------------------

app.include_router(user_router)

app.include_router(product_router)

app.include_router(health_router)


# -----------------------------
# HOME ENDPOINT
# -----------------------------

@app.get("/")
def home():

    return {

        "message": (
            "OPEN TELEMETRY FASTAPI APP"
        )

    }