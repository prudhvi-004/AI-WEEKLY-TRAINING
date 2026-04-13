# Import FastAPI framework → used to create APIs
from fastapi import FastAPI

# Import your models file (where you defined tables like Todo, User, etc.)
import model

# Import engine (DB connection) from your database.py file
from database import engine


# Create FastAPI app instance
# This is the main entry point of your API
app = FastAPI()


# Base → comes from declarative_base() in database.py
# metadata → stores info about all tables you created (like Todo table, etc.)

# create_all() → creates tables in the database
# bind=engine → tells SQLAlchemy WHICH database to create tables in

model.Base.metadata.create_all(bind=engine)