# Import function to create a connection (engine) to the database
from sqlalchemy import create_engine

# Import sessionmaker → used to create DB sessions (like a connection instance to talk to DB)
from sqlalchemy.orm import sessionmaker

# Import base class creator → used to define models (tables)
from sqlalchemy.ext.declarative import declarative_base


# Database URL → tells SQLAlchemy WHICH database to connect
# 'sqlite:///./todos.db'
# sqlite → database type
# /// → relative path
# ./todos.db → file will be created in current folder
SQLALCHEMY_DB_URL = 'sqlite:///./todos.db'


# create_engine → creates the actual connection to DB
# connect_args → extra settings (specific to SQLite here)
# check_same_thread=False → allows multiple threads (FastAPI uses multiple threads)
engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={'check_same_thread': False}
)


# sessionmaker → factory to create new DB sessions
# WHY needed?
# Instead of manually creating connections every time,
# we use this to generate sessions easily

SessionLocal = sessionmaker(
    autocommit=False,  # changes are NOT saved automatically → we control when to commit
    autoflush=False,   # changes are NOT sent to DB automatically → better control
    bind=engine        # bind session to our DB connection
)


# declarative_base → base class for all models (tables)
# WHY?
# All your table classes will inherit from this
# It helps SQLAlchemy know how to map Python class → DB table

Base = declarative_base()