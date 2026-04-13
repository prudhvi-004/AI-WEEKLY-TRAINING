# Import Base → parent class for all tables (comes from declarative_base)
from database import Base 

# Import Column and data types → used to define table structure
from sqlalchemy import Column, Integer, String, Boolean


# Create a class → represents a TABLE in database
# WHY class?
# Because SQLAlchemy maps Python class → DB table (ORM concept)
class Todos(Base):

    # Table name in database
    # WHY?
    # This is the actual name that will appear in SQLite (todos.db)
    __tablename__ = 'todo'


    # Column 1: id
    # Integer → number type
    # primary_key=True → uniquely identifies each row
    # index=True → makes searching faster (like adding index in DB)
    id = Column(Integer, primary_key=True, index=True)


    # Column 2: title
    # String → text type
    # Stores task title
    title = Column(String)


    # Column 3: description
    # String → text type
    # Stores more details about task
    description = Column(String)


    # Column 4: priority
    # Integer → number type
    # You can use values like 1 (high), 2 (medium), 3 (low)
    priority = Column(Integer)


    # Column 5: complete
    # Boolean → True/False
    # default=False → when new task is created, it is incomplete by default
    complete = Column(Boolean, default=False)