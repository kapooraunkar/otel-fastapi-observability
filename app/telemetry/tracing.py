# ---------------------------------------------------
# TELEMETRY / OBSERVABILITY SETUP
# ---------------------------------------------------
# This file initializes the observability system
# for the application.
#
# Responsibilities:
# - initialize Niriksha AI SDK
# - configure telemetry export pipeline
# - provide reusable tracer object
#
# Observability data such as:
# - traces
# - spans
# - request metadata
# can then be exported to Niriksha platform.


from opentelemetry import trace

import nirikshaai

from app.core.config import settings


# ---------------------------------------------------
# REUSABLE TRACER
# ---------------------------------------------------
# Tracer object used throughout application
# for manually creating spans.
#
# Manual spans are still used inside:
# - service layer
# - cache layer
# - database operations
#
# Niriksha SDK handles the underlying
# observability infrastructure internally.


tracer = trace.get_tracer(__name__)


# ---------------------------------------------------
# SETUP TRACING
# ---------------------------------------------------
# Initializes Niriksha AI SDK and connects
# application telemetry pipeline to
# remote observability platform.
#
# Configuration includes:
# - ingestion endpoint
# - API authentication
# - service identification
# - environment metadata


def setup_tracing():

    nirikshaai.init(

        # Niriksha platform dashboard
        endpoint="https://app.niriksha.ai",

        # telemetry ingestion endpoint
        otlp_endpoint="grpc-ingest.niriksha.ai:443",
       
        # API authentication key
        api_key=settings.NIRIKSHA_API_KEY,

        # service name shown in dashboard
        service_name=(
            "otel-fastapi-service"
        ),

        # current application environment
        environment=settings.APP_ENV,

        # enables LLM/AI observability features
        enable_llm=True,
    )