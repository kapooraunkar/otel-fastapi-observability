from fastapi import FastAPI
import asyncio
from router.users import router as user_router
from opentelemetry.instrumentation.requests import (
    RequestsInstrumentor
)
# OpenTelemetry imports
from opentelemetry import trace   # used to create traces and spans

from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
# TracerProvider = main tracing engine

from opentelemetry.sdk.trace.export import BatchSpanProcessor
# sends spans in batches instead of one by one
# improves performance

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter
)
# exporter that sends traces outside the app

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)
# automatically instruments FastAPI endpoints


# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------

app = FastAPI()


# ---------------------------------------------------
# OPEN TELEMETRY SETUP
# ---------------------------------------------------

trace.set_tracer_provider(

    TracerProvider(

        resource=Resource.create({

            # custom service name shown in Jaeger
            "service.name": "otel-fastapi-service"

        })
    )
)

# creates tracer object
# tracer creates and manages spans
tracer = trace.get_tracer(__name__)


# exporter endpoint
# sends traces to Jaeger OTLP endpoint
otlp_exporter = OTLPSpanExporter(

    endpoint="http://localhost:4318/v1/traces"

)


# connects spans to exporter
span_processor = BatchSpanProcessor(

    otlp_exporter

)


# attaches export pipeline to tracer system
# now traces actually leave the application
trace.get_tracer_provider().add_span_processor(span_processor)


# automatically traces FastAPI endpoints
# tracks:
# request start
# request end
# latency
# status codes
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

# helper functions simulate different layers
# of a real backend application


# ---------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------

@app.get("/")
def home():

    return {

        "message": "OPEN TELEMETRY FASTAPI APP"

    }

app.include_router(user_router)

@app.get("/products")
def get_products():

    products = [

        "Laptop",
        "Phone",
        "Keyboard"

    ]

    return {

        "products": products

    }


@app.get("/health")
def health_check():

    return {

        "status": "healthy"

    }