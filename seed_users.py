from database import SessionLocal
from database import User


# creates DB session
db = SessionLocal()


# sample users
users = [

    User(name="Arron"),
    User(name="John"),
    User(name="Alice")

]


# inserts users into DB
db.add_all(users)

# saves changes
db.commit()

# closes DB connection
db.close()


print("Users inserted successfully")