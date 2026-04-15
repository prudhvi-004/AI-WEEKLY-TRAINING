# =========================
# 🔹 IMPORTS
# =========================

from typing import Annotated
# WHY?
# Used to combine type + dependency (clean DI)

from pydantic import BaseModel, Field
# WHY?
# BaseModel → request validation
# Field → add constraints

from sqlalchemy.orm import Session
# WHY?
# DB session to interact with database

from fastapi import APIRouter, Depends, HTTPException, Path
# WHY?
# APIRouter → group routes
# Depends → dependency injection
# HTTPException → error handling
# Path → validate path parameters

from starlette import status
# WHY?
# Clean HTTP status codes

from model import Todos
# WHY?
# ORM model (table representation)

from database import SessionLocal
# WHY?
# DB connection factory

from .auth import get_current_user
# WHY?
# Extract logged-in user from JWT


# =========================
# 🔹 ROUTER
# =========================

router = APIRouter()
# WHY?
# Groups all todo-related APIs


# =========================
# 🔹 DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()   # open DB connection
    try:
        yield db          # give DB to API
    finally:
        db.close()        # close after request

# WHY?
# Prevents DB connection leaks


db_dependency = Annotated[Session, Depends(get_db)]
# WHY?
# Inject DB automatically


user_dependency = Annotated[dict, Depends(get_current_user)]
# WHY?
# Inject current user from JWT


# =========================
# 🔹 REQUEST MODEL
# =========================

class TodoRequest(BaseModel):

    title: str = Field(min_length=3)
    # WHY?
    # Avoid empty/short titles

    description: str = Field(min_length=3, max_length=100)
    # WHY?
    # Control input size

    priority: int = Field(gt=0, lt=6)
    # WHY?
    # Only allow 1–5 priority

    complete: bool
    # WHY?
    # Task status


# =========================
# 🔹 READ ALL TODOS
# =========================

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):

    # Check authentication
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    # Fetch only current user's todos
    return db.query(Todos)\
        .filter(Todos.owner_id == user.get('id'))\
        .all()

# THEORY:
# Multi-user system → must isolate data


# =========================
# 🔹 READ ONE TODO
# =========================

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency,
                    todo_id: int = Path(gt=0)):

    # Validate user
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    # Fetch todo with:
    # ✔ matching ID
    # ✔ belongs to current user
    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id'))\
        .first()

    if todo_model:
        return todo_model

    raise HTTPException(status_code=404, detail='Todo not found.')

# THEORY:
# Double filtering prevents unauthorized access


# =========================
# 🔹 CREATE TODO
# =========================

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    # Convert request → DB object
    todo_model = Todos(
        **todo_request.model_dump(),  # unpack fields
        owner_id=user.get('id')       # link to user
    )

    db.add(todo_model)
    db.commit()

# THEORY:
# model_dump() → converts Pydantic → dict


# =========================
# 🔹 UPDATE TODO
# =========================

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    # Get existing todo
    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id'))\
        .first()

    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found.')

    # Update fields
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

# THEORY:
# Ensures only owner can update


# =========================
# 🔹 DELETE TODO
# =========================

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency,
                      todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    # Check existence
    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id'))\
        .first()

    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found.')

    # Delete
    db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id'))\
        .delete()

    db.commit()

# THEORY:
# Prevents deleting others’ data