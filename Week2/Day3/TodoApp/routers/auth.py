from fastapi import APIRouter,Depends, HTTPException
from model import Users
from pydantic import BaseModel
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta,datetime,timezone

router = APIRouter(prefix='/auth',tags=['auth'])

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') #my app uses OAuth2bearer tokens & user will get their token from this url("token").

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str 
    role: str


#it’s the response structure for your login API.
class Token(BaseModel):
    access_token: str
    token_type: str


# Dependency function to provide database session to API routes
def get_db():
    
    # 🔹 Create a new database session (connection)
    # 👉 SessionLocal is a factory that creates DB sessions
    db = SessionLocal()
    
    try:
        # 🔹 Provide the DB session to the API
        # 👉 'yield' sends db to wherever this dependency is used
        # 👉 Execution pauses here until the API finishes
        yield db 
    
    finally:
        # 🔹 This block runs AFTER the API request is completed
        # 👉 Ensures the DB connection is properly closed
        # 👉 Prevents memory leaks and too many open connections
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]  #to get a db session inside a funtion so we can perform operations.

#2 --> it is an function
def authenticate_user(username: str, password: str, db):
    # 🔹 Step 1: Query the database to find a user with the given username
    # db = SQLAlchemy Session (used to interact with DB)
    # Users = your table/model
    user = db.query(Users).filter(Users.username == username).first()

    # 🔹 Step 2: If user does not exist → return False
    # Means authentication failed (wrong username)
    if not user:
        return False

    # 🔹 Step 3: Verify password
    # bcrypt_context.verify() compares:
    #   plain password (entered by user)
    #   hashed password (stored in DB)
    # If password is incorrect → return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    # 🔹 Step 4: If both checks pass → authentication successful
    # Instead of returning True, we return the user object
    # so we can use user details later (like id, username, etc.)
    return user

#3 ---> Create JWT token and it is an function
def create_access_token(username: str, user_id: int, expires_delta: timedelta):

    encode = {
        'sub': username,
        'id': user_id   
          }
    expires = datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


#5 ---> to get current user by JWT token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
       payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
       username: str = payload.get('sub')
       user_id: int = payload.get('id')
       if username is None or user_id is None:
           raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                               detail  = 'Could Not validate User')
       return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                               detail  = 'Could Not validate User')
        
           

#1
#creating a user and adding into db
@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
    create_user_request: CreateUserRequest):

    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

 
#4 ---> authenticate user using Auth function and if user exist it creates a access jwt  token for that user and it will return..
@router.post('/token',response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                               detail  = 'Could Not validate User')
    access_token = create_access_token(user.username,user.id,timedelta(minutes=20))
    return {'access_token':access_token ,'token_type':'bearer'}
    
