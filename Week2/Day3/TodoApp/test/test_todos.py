# =========================
# 🔹 IMPORTS
# =========================

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from model import Base, Todos

# MUST match dependencies used in todos.py
from routers.todos import get_db
from routers.auth import get_current_user

import pytest
from fastapi import status
from fastapi.testclient import TestClient


# =========================
# 🔹 TEST DATABASE SETUP
# =========================

SQLALCHEMY_TEST_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

Test_SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create tables
Base.metadata.create_all(bind=engine)


# =========================
# 🔹 DEPENDENCY OVERRIDES
# =========================

def override_get_db():
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'bablu', 'id': 1, 'role': 'admin'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# =========================
# 🔹 TEST CLIENT
# =========================

client = TestClient(app)


# =========================
# 🔹 FIXTURE (TEST DATA)
# =========================

@pytest.fixture
def test_todo():
    db = Test_SessionLocal()

    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo

    # cleanup after test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# =========================
# 🔹 TEST: GET ALL
# =========================

def test_read_all_authenticated(test_todo):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }]


# =========================
# 🔹 TEST: GET ONE
# =========================

def test_read_one_authenticated(test_todo):
    response = client.get("/1")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['id'] == 1
    assert data['owner_id'] == 1


# =========================
# 🔹 TEST: NOT FOUND
# =========================

def test_read_one_authenticated_not_found():
    response = client.get("/999")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


# =========================
# 🔹 TEST: CREATE
# =========================

def test_create_todo():
    request_data = {
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post("/addtodo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = Test_SessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == request_data['title']


# =========================
# 🔹 TEST: UPDATE
# =========================

def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated Title',
        'description': 'Updated Desc',
        'priority': 5,
        'complete': False,
    }

    response = client.put("/updatetodo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = Test_SessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == 'Updated Title'


# =========================
# 🔹 TEST: UPDATE NOT FOUND
# =========================

def test_update_todo_not_found():
    request_data = {
        'title': 'Updated Title',
        'description': 'Updated Desc',
        'priority': 5,
        'complete': False,
    }

    response = client.put("/updatetodo/999", json=request_data)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


# =========================
# 🔹 TEST: DELETE
# =========================

def test_delete_todo(test_todo):
    response = client.delete("/deletetodo/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = Test_SessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


# =========================
# 🔹 TEST: DELETE NOT FOUND
# =========================

def test_delete_todo_not_found():
    response = client.delete("/deletetodo/999")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}