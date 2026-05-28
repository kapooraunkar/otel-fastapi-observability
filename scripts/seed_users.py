# ---------------------------------------------------
# DATABASE SEED SCRIPT
# ---------------------------------------------------
# This script inserts sample users into database.
#
# Seed scripts are commonly used for:
# - testing
# - development setup
# - demo/sample data
#
# Instead of manually creating records every time,
# we can quickly populate database with initial data.


from app.db.database import SessionLocal

from app.models.user_model import User


# ---------------------------------------------------
# CREATE DATABASE SESSION
# ---------------------------------------------------
# Opens temporary database session
# used for performing insert operations.


db = SessionLocal()


# ---------------------------------------------------
# SAMPLE USERS
# ---------------------------------------------------
# SQLAlchemy User model instances
# that will be inserted into database.


users = [

    User(name="Arron"),

    User(name="John"),

    User(name="Alice")
]


# ---------------------------------------------------
# INSERT USERS
# ---------------------------------------------------
# add_all() stages all objects
# for insertion into database.


db.add_all(users)


# ---------------------------------------------------
# COMMIT CHANGES
# ---------------------------------------------------
# commit() permanently saves
# changes into database.


db.commit()


# ---------------------------------------------------
# CLOSE DATABASE SESSION
# ---------------------------------------------------
# Releases database connection resources.


db.close()


print("Users inserted successfully")