from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# PostgreSQL connection URL
DATABASE_URL = ("postgresql://postgres:postgres@localhost:5432/otel_db")


# creates DB engine
engine = create_engine(DATABASE_URL)   #connects python to database


# creates DB sessions
SessionLocal = sessionmaker(

    autocommit=False,
    autoflush=False,
    bind=engine

)


# base class for models/tables
Base = declarative_base()


# users table
class User(Base):  

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  #id column, integer datatype, unique ID

    name = Column(String)  #name column, string type


# creates tables in PostgreSQL
Base.metadata.create_all(bind=engine)