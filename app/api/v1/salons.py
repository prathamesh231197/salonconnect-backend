# app/api/v1/salons.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from typing import Optional

from db.session import SessionLocal
from crud.salon import create_salon, get_salon, list_salons
from core.security import decode_access_token
from crud.user import get_user_by_email
from schemas import SalonCreate, SalonOut

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db), authorization: Optional[str] = None):
    """
    Lightweight token dependency: we read Authorization header manually because
    we want a simple dependency here. FastAPI usually uses OAuth2PasswordBearer,
    but to keep things explicit we accept token via header.
    """
    # This dependency will be used only in POST /api/salons (create). For GETs we allow public listing.
    # FastAPI will inject header into 'authorization' if provided via Depends, but a simpler way:
    return None

# Helper to extract token from header within endpoint (simpler & explicit)


def _get_user_from_auth_header(authorization: Optional[str], db: Session):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authorization header required")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization header")
    token = parts[1]
    email = decode_access_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("", response_model=SalonOut, status_code=status.HTTP_201_CREATED)
def create_salon_endpoint(salon_in: SalonCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    # require Authorization header: "Bearer <token>"
    user = _get_user_from_auth_header(authorization, db)
    salon = create_salon(db, owner_id=user.id, salon_in=salon_in)
    return salon


@router.get("", response_model=list[SalonOut])
def list_salons_endpoint(q: Optional[str] = Query(None), limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    salons = list_salons(db, q=q, limit=limit, offset=offset)
    return salons


@router.get("/{salon_id}", response_model=SalonOut)
def get_salon_endpoint(salon_id: int, db: Session = Depends(get_db)):
    salon = get_salon(db, salon_id)
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Salon not found")
    return salon
