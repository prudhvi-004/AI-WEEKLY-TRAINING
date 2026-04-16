# Import Base → parent class for all tables
from database import Base 

# Import Column and data types
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):

    __tablename__ = 'users'

    # ✅ FIX: change String → Integer (auto-increment works now)
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

    # Optional improvement: default value
    is_active = Column(Boolean, default=True)

    role = Column(String)


class Todos(Base):

    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

    # ✅ This will now correctly link to Users.id
    owner_id = Column(Integer, ForeignKey('users.id'))