from fastapi import FastAPI
import asyncio

from opentelemetry import trace

from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter
)

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)

app = FastAPI()


# -----------------------------
# OTEL SETUP
# -----------------------------

trace.set_tracer_provider(

    TracerProvider(

        resource=Resource.create({

            "service.name": "user-service"

        })
    )
)

tracer = trace.get_tracer(__name__)


otlp_exporter = OTLPSpanExporter(

    endpoint="http://localhost:4318/v1/traces"

)

span_processor = BatchSpanProcessor(
    otlp_exporter
)

trace.get_tracer_provider().add_span_processor(
    span_processor
)

FastAPIInstrumentor.instrument_app(app)


# -----------------------------
# ENDPOINT
# -----------------------------

@app.get("/internal-users")
async def internal_users():

    with tracer.start_as_current_span("fetch-users-from-db"):

        await asyncio.sleep(0.5)

    return {

        "users": [
            "Arron",
            "John",
            "Alice"
        ]
    }