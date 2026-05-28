# ---------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------
# This file sets up:
# - database connection
# - SQLAlchemy engine
# - database sessions
# - base ORM model class
#
# It acts as the central database layer
# used throughout the application.


from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from app.core.config import settings


# load environment variables from .env
load_dotenv()


# database connection URL
DATABASE_URL = settings.DATABASE_URL


# ---------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------
# SQLAlchemy engine manages the actual
# connection between application and database.
#
# Engine acts as the core interface used
# for executing database operations.


engine = create_engine(

    DATABASE_URL

)


# ---------------------------------------------------
# DATABASE SESSION FACTORY
# ---------------------------------------------------
# SessionLocal creates new database sessions.
#
# Database sessions are temporary conversations
# between application and database.
#
# Each request gets its own session.


SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)


# ---------------------------------------------------
# DATABASE DEPENDENCY
# ---------------------------------------------------
# Provides database session to FastAPI endpoints
# using dependency injection.
#
# Flow:
# 1. create database session
# 2. provide session to endpoint/service
# 3. automatically close session afterward
#
# This prevents database connection leaks.


def get_db():

    db = SessionLocal()

    try:

        # temporarily provide database session
        yield db

    finally:

        # cleanup database connection
        db.close()


# ---------------------------------------------------
# BASE ORM MODEL
# ---------------------------------------------------
# Base class inherited by all SQLAlchemy models.
#
# Example:
# class User(Base)
#
# SQLAlchemy uses this base class to track
# database tables/models.


Base = declarative_base()