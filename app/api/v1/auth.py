# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.session import SessionLocal
from schemas import UserCreate, Token
from crud.user import get_user_by_email, create_user, verify_password
from core.security import create_access_token

router = APIRouter()

# Dependency to get DB Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginIn(BaseModel):
    email: str
    password: str


@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, email=payload.email, password=payload.password,
                       name=payload.name, phone=payload.phone)
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
