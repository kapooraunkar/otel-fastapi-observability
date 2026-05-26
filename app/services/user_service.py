from app.database import SessionLocal

from app.models.user_model import User

from app.telemetry.tracing import tracer


# in-memory cache
cache_store = {}


# -----------------------------
# CACHE LAYER
# -----------------------------

async def check_cache():

    with tracer.start_as_current_span("cache-check") as span:

        users = cache_store.get("users")

        # cache hit
        if users:

            span.set_attribute("cache.hit", True)

            span.add_event("Cache HIT")

            return users

        # cache miss
        span.set_attribute("cache.hit", False)

        span.add_event("Cache MISS")

        return None


# -----------------------------
# DATABASE QUERY
# -----------------------------

async def query_database():

    with tracer.start_as_current_span("database-query") as span:

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

        db = SessionLocal()

        users = db.query(User).all()

        db.close()

        return [

            user.name

            for user in users
        ]


# -----------------------------
# FETCH USERS
# -----------------------------

async def fetch_users():

    # check cache first
    cached_users = await check_cache()

    # cache hit
    if cached_users:

        return cached_users

    # cache miss
    users = await query_database()

    # save into cache
    cache_store["users"] = users

    return users


# -----------------------------
# CREATE USER
# -----------------------------

async def create_new_user(name: str):

    with tracer.start_as_current_span("create-user"):

        db = SessionLocal()

        # database insert span
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

            new_user = User(name=name)

            db.add(new_user)

            db.commit()

        db.close()

        # clear cache after insert
        cache_store.clear()

        return {

            "message": (
                f"{name} added successfully"
            )

        }