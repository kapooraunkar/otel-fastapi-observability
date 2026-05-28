from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from app.db.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index= True)   #create a column with integer data type, a primary key and give it an index

    name = Column(String,index=True) #a column with string data type and index it to find it easily later


