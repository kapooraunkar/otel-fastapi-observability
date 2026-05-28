# ---------------------------------------------------
# USER API ROUTES
# ---------------------------------------------------
# This file contains all user-related API endpoints.
#
# Routers handle:
# - incoming HTTP requests
# - request validation
# - dependency injection
# - response formatting
#
# Actual business logic is delegated to
# service layer functions.


from fastapi import APIRouter

from fastapi import Depends

from sqlalchemy.orm import Session


# database dependency
from app.db.database import (
    get_db
)


# request/response schemas
from app.schema.user_schema import (

    UserCreate,

    UserResponse
)


# service layer functions
from app.services.user_service import (

    fetch_users,

    create_new_user
)


# ---------------------------------------------------
# ROUTER CONFIGURATION
# ---------------------------------------------------
# prefix="/api/v1"
# automatically adds API versioning
# to all endpoints inside this router.
#
# Example:
# /users
# becomes:
# /api/v1/users
#
# tags=["Users"]
# groups endpoints nicely inside Swagger UI.


router = APIRouter(

    prefix="/api/v1",

    tags=["Users"]
)


# ---------------------------------------------------
# GET USERS ENDPOINT
# ---------------------------------------------------
# Returns all users.
#
# Flow:
# request
# → router
# → service layer
# → cache/database
# → response
#
# FastAPI automatically injects database session
# using Depends(get_db).


@router.get(

    "/users",

    response_model=UserResponse
)

async def get_users(

    db: Session = Depends(get_db)

):

    users = await fetch_users(db)

    return {

        "users": users

    }


# ---------------------------------------------------
# CREATE USER ENDPOINT
# ---------------------------------------------------
# Creates new user inside database.
#
# UserCreate schema validates incoming request body.
#
# Example request:
# {
#     "name": "Alice"
# }


@router.post("/users")

async def create_user(

    user: UserCreate,

    db: Session = Depends(get_db)

):

    return await create_new_user(

        user.name,

        db
    )