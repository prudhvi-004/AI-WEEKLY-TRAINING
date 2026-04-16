# =========================
# 🔹 IMPORTS
# =========================

from datetime import timedelta, datetime, timezone
# datetime → get current time
# timedelta → define expiry duration
# timezone → ensures UTC time (important for JWT)

from typing import Annotated
# Annotated → combines type + dependency (modern FastAPI style)

from fastapi import APIRouter, Depends, HTTPException
# APIRouter → group routes (/auth)
# Depends → dependency injection (auto-run functions)
# HTTPException → return API errors

from pydantic import BaseModel, Field
# BaseModel → validates request body
# Field → adds rules (min length, etc.)

from sqlalchemy.orm import Session
# Session → DB connection object

from starlette import status
# status → HTTP status codes (401, 201, etc.)

from database import SessionLocal
# SessionLocal → creates DB session

from model import Users
# Users → your DB table (ORM model)

from passlib.context import CryptContext
# CryptContext → handles password hashing

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# OAuth2PasswordRequestForm → reads username & password (LOGIN FORM)
# OAuth2PasswordBearer → reads token from request header

from jose import jwt, JWTError
# jwt → create & decode token
# JWTError → handle token errors


# =========================
# 🔹 ROUTER SETUP
# =========================

router = APIRouter(
    prefix="/auth",   # All endpoints start with /auth
    tags=["Auth"]     # Group name in Swagger UI
)

# 🔥 WHAT THIS BLOCK DOES:
# Groups all authentication APIs together
# Example:
# /auth/token
# /auth/


# =========================
# 🔹 SECURITY CONFIG
# =========================

SECRET_KEY = "your-secret-key"
# 🔐 Used to SIGN JWT (very important)

ALGORITHM = "HS256"
# 🔐 Algorithm used to encode JWT

bcrypt_context = CryptContext(
    schemes=["bcrypt"],   # use bcrypt hashing
    deprecated="auto"
)

# 🔥 WHAT THIS BLOCK DOES:
# Defines how passwords will be hashed & verified


oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)

# 🔥 WHAT THIS BLOCK DOES:
# Extracts JWT token from request header:
# Authorization: Bearer <token>


# =========================
# 🔹 Pydantic MODELS
# =========================

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=5)
    role: str

# 🔥 WHAT THIS BLOCK DOES:
# Validates incoming user data when creating account


class Token(BaseModel):
    access_token: str
    token_type: str

# 🔥 WHAT THIS BLOCK DOES:
# Defines login response structure


# =========================
# 🔹 DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()   # create DB connection
    try:
        yield db          # give DB to API
    finally:
        db.close()        # always close connection

# 🔥 WHAT THIS BLOCK DOES:
# Manages DB lifecycle (open → use → close)


db_dependency = Annotated[Session, Depends(get_db)]

# 🔥 WHAT THIS BLOCK DOES:
# Shortcut so we can just write:
# db: db_dependency


# =========================
# 🔹 AUTH FUNCTION
# =========================

def authenticate_user(username: str, password: str, db):

    # 🔹 Get user from DB
    user = db.query(Users).filter(Users.username == username).first()

    # 🔹 If user not found
    if not user:
        return False

    # 🔹 Verify password
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    # 🔹 If everything is correct
    return user

# 🔥 WHAT THIS BLOCK DOES:
# Checks:
# ✔ user exists
# ✔ password is correct


# =========================
# 🔹 CREATE JWT TOKEN
# =========================

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {
        "sub": username,   # subject (main identity)
        "id": user_id,
        "role": role
    }

    # 🔹 Add expiry
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    # 🔹 Create token
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔥 WHAT THIS BLOCK DOES:
# Creates JWT token containing user info


# =========================
# 🔹 GET CURRENT USER (LOCK) BY JWT TOKEN
# =========================

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        # 🔹 Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")

        # 🔹 If token invalid
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "username": username,
            "id": user_id,
            "role": role
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 🔥 WHAT THIS BLOCK DOES:
# 🔐 PROTECTS ROUTES
# ✔ Extract token
# ✔ Decode token
# ✔ Return user info


# =========================
# 🔹 CREATE USER API
# =========================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    # 🔹 Check duplicate user
    existing_user = db.query(Users).filter(
        Users.username == create_user_request.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # 🔹 Create user
    new_user = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,

        # 🔐 Hash password
        hashed_password=bcrypt_context.hash(create_user_request.password),

        is_active=True
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

# 🔥 WHAT THIS BLOCK DOES:
# Registers user with hashed password


# =========================
# 🔹 LOGIN API (IMPORTANT BLOCK)
# =========================

@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):

    # 🔥 IMPORTANT BLOCK
    # form_data automatically gives:
    # form_data.username
    # form_data.password

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=20)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# 🔥 WHAT THIS BLOCK DOES:
# ✔ Takes username & password (FORM DATA)
# ✔ Validates user
# ✔ Generates JWT token
# ✔ Returns token to client