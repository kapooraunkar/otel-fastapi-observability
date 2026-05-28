# ---------------------------------------------------
# PYDANTIC SCHEMAS
# ---------------------------------------------------
# Schemas define the structure of:
# - incoming request data
# - outgoing API responses
#
# FastAPI uses these schemas for:
# - request validation
# - automatic documentation
# - response formatting


from pydantic import BaseModel

from typing import List


# ---------------------------------------------------
# CREATE USER REQUEST SCHEMA
# ---------------------------------------------------
# Validates incoming request data
# while creating new user.
#
# Example:
# {
#     "name": "Alice"
# }


class UserCreate(BaseModel):

    name: str


# ---------------------------------------------------
# USER RESPONSE SCHEMA
# ---------------------------------------------------
# Defines response structure returned
# by GET users endpoint.
#
# Example:
# {
#     "users": ["Alice", "John"]
# }


class UserResponse(BaseModel):

    users: List[str]