# ---------------------------------------------------
# APPLICATION CONFIGURATION
# ---------------------------------------------------
# Centralized configuration management.
#
# This file loads environment variables
# from .env file and exposes them through
# a reusable Settings object.
#
# Keeping configuration centralized helps:
# - avoid hardcoding secrets
# - support multiple environments
# - simplify deployment configuration
#
# Example environments:
# - development
# - staging
# - production


from dotenv import load_dotenv

import os


# load environment variables from .env file
load_dotenv()


# ---------------------------------------------------
# SETTINGS CLASS
# ---------------------------------------------------
# Stores reusable application configuration values.
#
# Environment variables are used instead of
# hardcoding sensitive values directly in code.


class Settings:


    # database connection URL
    DATABASE_URL = os.getenv(

        "DATABASE_URL"
    )


    # OpenTelemetry exporter endpoint
    OTEL_EXPORTER_ENDPOINT = os.getenv(

        "OTEL_EXPORTER_ENDPOINT"
    )


    # Niriksha AI API key used for
    # observability authentication
    NIRIKSHA_API_KEY = os.getenv(

        "NIRIKSHA_API_KEY"
    )


    # current application environment
    # defaults to "development"
    APP_ENV = os.getenv(

        "APP_ENV",

        "development"
    )


# reusable settings object
settings = Settings()