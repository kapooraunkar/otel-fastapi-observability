from fastapi import APIRouter

from database import SessionLocal
from database import User

from opentelemetry import trace


router = APIRouter()

tracer = trace.get_tracer(__name__)

cache_store = {}


# cache layer
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


# database layer
async def query_database():

    with tracer.start_as_current_span("database-query") as span:
        print("DATABASE QUERY EXECUTED")

        span.set_attribute("db.system", "postgresql")

        span.set_attribute("db.operation", "SELECT")

        span.set_attribute("db.table", "users")

        db = SessionLocal()

        users = db.query(User).all()

        db.close()

        return [

            user.name

            for user in users
        ]


@router.post("/users")
async def create_user(name: str):

    with tracer.start_as_current_span("create-user"):

        db = SessionLocal()

        with tracer.start_as_current_span("database-insert") as span:

            span.set_attribute("db.system", "postgresql")

            span.set_attribute("db.operation", "INSERT")

            span.set_attribute("db.table", "users")

            new_user = User(name=name)

            db.add(new_user)

            db.commit()

        db.close()

        cache_store.clear()

        return {

            "message": f"{name} added successfully"

        }
@router.get("/users")
async def get_users():

    # check cache first
    cached_users = await check_cache()

    # cache hit
    if cached_users:

        return {
            "users": cached_users
        }

    # cache miss
    users = await query_database()

    # save users into cache
    cache_store["users"] = users

    return {
        "users": users
    }