from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from ..db import SessionLocal
from ..models import User
from pydantic import BaseModel

SECRET_KEY = "4f3c9e7c5d8f69b2eebc3d6a1b9e56d8d2f8e5c4a3d1f9b7c2a6e4d3b8f1e0c7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserCreate(BaseModel):
    username: str
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """User login."""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
