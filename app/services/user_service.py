# ---------------------------------------------------
# USER SERVICE LAYER
# ---------------------------------------------------
# This file contains the main business logic
# related to users.
#
# Responsibilities:
# - cache handling
# - database queries
# - observability tracing
# - logging
#
# Routers/endpoints call functions from this file
# instead of directly talking to database.
#
# This separation keeps application architecture
# cleaner and easier to scale.


from sqlalchemy.orm import Session

from app.models.user_model import User

from app.telemetry.tracing import tracer

from app.core.logging_config import logger


# ---------------------------------------------------
# IN-MEMORY CACHE
# ---------------------------------------------------
# Simple temporary cache stored in memory.
#
# Used to avoid repeated database queries
# for frequently accessed user data.
#
# Real production systems usually use:
# - Redis
# - Memcached
# - distributed caching systems


cache_store = {}


# ---------------------------------------------------
# CACHE CHECK
# ---------------------------------------------------
# Checks whether users data already exists
# inside cache memory.
#
# Cache hit:
# data found in memory
#
# Cache miss:
# data not found → query database


async def check_cache():

    with tracer.start_as_current_span(
        "cache-check"
    ) as span:

        users = cache_store.get("users")

        # cache hit
        if users:

            span.set_attribute(
                "cache.hit",
                True
            )

            span.add_event("Cache HIT")

            logger.info(
                "Cache HIT for users"
            )

            return users

        # cache miss
        span.set_attribute(
            "cache.hit",
            False
        )

        span.add_event("Cache MISS")

        logger.info(
            "Cache MISS for users"
        )

        return None


# ---------------------------------------------------
# DATABASE QUERY
# ---------------------------------------------------
# Fetches users from PostgreSQL database.
#
# OpenTelemetry span attributes provide
# metadata about:
# - database type
# - operation type
# - table being queried
#
# This helps observability platforms
# understand database behavior.


async def query_database(
    db: Session
):

    with tracer.start_as_current_span(
        "database-query"
    ) as span:

        span.set_attribute(
            "db.system",
            "postgresql"
        )

        span.set_attribute(
            "db.operation",
            "SELECT"
        )

        span.set_attribute(
            "db.table",
            "users"
        )

        logger.info(
            "Executing users database query"
        )

        users = db.query(User).all()

        return [

            user.name

            for user in users
        ]


# ---------------------------------------------------
# FETCH USERS
# ---------------------------------------------------
# Main user fetching workflow.
#
# Flow:
# 1. check cache
# 2. if cache hit → return cached data
# 3. if cache miss → query database
# 4. store database result in cache


async def fetch_users(
    db: Session
):

    # check cache first
    cached_users = await check_cache()

    # cache hit
    if cached_users:

        return cached_users

    # cache miss
    users = await query_database(db)

    # save users into cache
    cache_store["users"] = users

    return users


# ---------------------------------------------------
# CREATE USER
# ---------------------------------------------------
# Creates new user inside database.
#
# Also clears cache after insertion
# so future requests fetch fresh data
# instead of outdated cached users.


async def create_new_user(
    name: str,
    db: Session
):

    with tracer.start_as_current_span(
        "create-user"
    ):

        # trace database insert operation
        with tracer.start_as_current_span(
            "database-insert"
        ) as span:

            span.set_attribute(
                "db.system",
                "postgresql"
            )

            span.set_attribute(
                "db.operation",
                "INSERT"
            )

            span.set_attribute(
                "db.table",
                "users"
            )

            logger.info(
                f"Creating new user: {name}"
            )

            new_user = User(name=name)

            db.add(new_user)

            db.commit()

        # clear cache after insertion
        cache_store.clear()

        return {

            "message": (
                f"{name} added successfully"
            )

        }