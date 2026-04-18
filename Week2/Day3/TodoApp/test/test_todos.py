# =========================
# IMPORTS
# =========================

# create_engine is used to create database connection
# text is used to run raw SQL queries (for cleanup)
from sqlalchemy import create_engine, text

# sessionmaker is used to create database sessions
from sqlalchemy.orm import sessionmaker

# StaticPool ensures a single shared connection (important for SQLite tests)
from sqlalchemy.pool import StaticPool

# importing main FastAPI app
from main import app

# Base is used to create tables, Todos is the ORM model
from model import Base, Todos

# importing dependencies to override (used in todos API)
from routers.todos import get_db
from routers.auth import get_current_user

# pytest is used for testing framework
import pytest

# status provides HTTP status codes
from fastapi import status

# TestClient simulates API requests without running server
from fastapi.testclient import TestClient


# =========================
# TEST DATABASE SETUP
# =========================

# separate database used only for testing
SQLALCHEMY_TEST_URL = 'sqlite:///./testdb.db'

# creating database engine
engine = create_engine(
    SQLALCHEMY_TEST_URL,

    # allows multiple threads to access SQLite
    connect_args={'check_same_thread': False},

    # ensures all sessions share same connection
    poolclass=StaticPool
)

# creating session factory
Test_SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# creating tables in test database
Base.metadata.create_all(bind=engine)


# =========================
# OVERRIDES (NO DEEP EXPLANATION)
# =========================

def override_get_db():
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'bablu', 'id': 1, 'role': 'admin'}


# applying overrides to FastAPI app
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# =========================
# TEST CLIENT
# =========================

# client will behave like a user calling the API
client = TestClient(app)


# =========================
# FIXTURE (TEST DATA SETUP)
# =========================

@pytest.fixture
def test_todo():

    # create DB session
    db = Test_SessionLocal()

    # create sample todo object
    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )

    # insert data into DB
    db.add(todo)
    db.commit()

    # refresh ensures ID is generated and synced
    db.refresh(todo)

    # provide this object to tests
    yield todo

    # cleanup after test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# =========================
# TEST: GET ALL TODOS
# =========================

def test_read_all_authenticated(test_todo):

    # call API endpoint to get all todos
    response = client.get("/")

    # check response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # check response data matches expected output
    assert response.json() == [{
        'id': 1,
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }]


# =========================
# TEST: GET SINGLE TODO
# =========================

def test_read_one_authenticated(test_todo):

    # call API to get todo with id=1
    response = client.get("/1")

    # check status code
    assert response.status_code == status.HTTP_200_OK

    # get response data
    data = response.json()

    # validate important fields
    assert data['id'] == 1
    assert data['owner_id'] == 1


# =========================
# TEST: TODO NOT FOUND
# =========================

def test_read_one_authenticated_not_found():

    # call API with non-existing ID
    response = client.get("/999")

    # check status code is 404
    assert response.status_code == 404

    # check error message
    assert response.json() == {'detail': 'Todo not found.'}


# =========================
# TEST: CREATE TODO
# =========================

def test_create_todo():

    # request data to create new todo
    request_data = {
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    # call API to create todo
    response = client.post("/addtodo", json=request_data)

    # check status code is 201 CREATED
    assert response.status_code == status.HTTP_201_CREATED

    # verify data is stored in database
    db = Test_SessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    # check stored data
    assert model.title == request_data['title']


# =========================
# TEST: UPDATE TODO
# =========================

def test_update_todo(test_todo):

    # updated data
    request_data = {
        'title': 'Updated Title',
        'description': 'Updated Desc',
        'priority': 5,
        'complete': False,
    }

    # call API to update todo
    response = client.put("/updatetodo/1", json=request_data)

    # check status code is 204 (no content)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # verify update in database
    db = Test_SessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    # check updated value
    assert model.title == 'Updated Title'


# =========================
# TEST: UPDATE NOT FOUND
# =========================

def test_update_todo_not_found():

    # updated data
    request_data = {
        'title': 'Updated Title',
        'description': 'Updated Desc',
        'priority': 5,
        'complete': False,
    }

    # call API with non-existing ID
    response = client.put("/updatetodo/999", json=request_data)

    # check status code
    assert response.status_code == 404

    # check error message
    assert response.json() == {'detail': 'Todo not found.'}


# =========================
# TEST: DELETE TODO
# =========================

def test_delete_todo(test_todo):

    # call API to delete todo
    response = client.delete("/deletetodo/1")

    # check status code
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # verify deletion from database
    db = Test_SessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    # should be None after deletion
    assert model is None


# =========================
# TEST: DELETE NOT FOUND
# =========================

def test_delete_todo_not_found():

    # call API with non-existing ID
    response = client.delete("/deletetodo/999")

    # check status code
    assert response.status_code == 404

    # check error response
    assert response.json() == {'detail': 'Todo not found.'}