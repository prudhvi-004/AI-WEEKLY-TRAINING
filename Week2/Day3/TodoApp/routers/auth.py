# =========================
# 🔹 IMPORTS
# =========================

# Time handling (used for token expiry)
from datetime import timedelta, datetime, timezone

# Used to attach dependencies cleanly
from typing import Annotated

# FastAPI core tools
from fastapi import APIRouter, Depends, HTTPException

# Used for request validation
from pydantic import BaseModel

# DB session handling
from sqlalchemy.orm import Session

# HTTP status codes (like 401, 201)
from starlette import status

# DB connection factory
from database import SessionLocal

# Users table (ORM model)
from model import Users

# Password hashing tool
from passlib.context import CryptContext

# OAuth2 tools
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# JWT encoding/decoding
from jose import jwt, JWTError


# =========================
# 🔹 ROUTER SETUP
# =========================

router = APIRouter(
    prefix='/auth',   # all routes start with /auth
    tags=['Auth']     # shown in Swagger UI
)

# WHY?
# Keeps authentication routes grouped and organized


# =========================
# 🔹 SECURITY CONFIG
# =========================

SECRET_KEY = 'your-secret-key'
# WHY?
# Used to sign JWT → prevents tampering

ALGORITHM = 'HS256'
# WHY?
# Encryption algorithm for JWT


bcrypt_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)
# WHY?
# Hash passwords securely


oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl='auth/token'
)
# WHY?
# Extracts token from Authorization header


# =========================
# 🔹 MODELS (DATA VALIDATION)
# =========================

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

# WHY?
# Validates incoming user data automatically


class Token(BaseModel):
    access_token: str
    token_type: str

# WHY?
# Defines response structure for login


# =========================
# 🔹 DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()   # open DB connection
    try:
        yield db          # send DB to API
    finally:
        db.close()        # close after request

# WHY?
# Avoids memory leaks and manages DB lifecycle


db_dependency = Annotated[Session, Depends(get_db)]
# WHY?
# Cleaner way to inject DB into routes


# =========================
# 🔹 AUTHENTICATION FUNCTION
# =========================

def authenticate_user(username: str, password: str, db):

    # Find user in DB
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    # Verify password (plain vs hashed)
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user

# WHY?
# Ensures login credentials are correct


# =========================
# 🔹 CREATE JWT TOKEN
# =========================

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    # Payload (data inside token)
    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }

    # Expiry time
    expires = datetime.now(timezone.utc) + expires_delta

    # Add expiry
    encode.update({'exp': expires})

    # Generate token
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# WHY?
# Token carries user identity securely


# =========================
# 🔹 GET CURRENT USER
# =========================

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user info
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')

        # If invalid token
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate user.')

        return {
            'username': username,
            'id': user_id,
            'user_role': user_role
        }

    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')

# WHY?
# Protects routes by verifying JWT


# =========================
# 🔹 CREATE USER API
# =========================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,

        # Hash password before storing
        hashed_password=bcrypt_context.hash(create_user_request.password),

        is_active=True
    )

    db.add(create_user_model)
    db.commit()

# WHY?
# Registers user securely


# =========================
# 🔹 LOGIN API
# =========================

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):

    # Validate user
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail='Could not validate user.')

    # Create token
    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=20)
    )

    return {
        'access_token': token,
        'token_type': 'bearer'
    }

# WHY?
# Allows user to login and get JWT token