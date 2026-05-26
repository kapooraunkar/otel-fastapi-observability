from fastapi import APIRouter

from app.services.user_service import (
    fetch_users
)

from app.services.user_service import (
    create_new_user
)


# router object
router = APIRouter()


# -----------------------------
# GET USERS
# -----------------------------

@router.get("/users")
async def get_users():

    users = await fetch_users()

    return {

        "users": users

    }


# -----------------------------
# CREATE USER
# -----------------------------

@router.post("/users")
async def create_user(name: str):

    return await create_new_user(name)