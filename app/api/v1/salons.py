# app/api/v1/salons.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field

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


def _get_user_from_auth_header(authorization: Optional[str], db: Session):
    """
    Extract bearer token, decode, and return user object from DB.
    Raises 401 if header missing/invalid or user not found.
    """
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


# --- serializers (ensure endpoints return plain dicts that match SalonOut) ---
def _serialize_service(svc) -> dict:
    if svc is None:
        return None
    return {
        "id": getattr(svc, "id", None),
        "name": getattr(svc, "name", None),
        "description": getattr(svc, "description", None),
        "duration_minutes": getattr(svc, "duration_minutes", None),
        "price": float(getattr(svc, "price", 0.0)) if getattr(svc, "price", None) is not None else None,
    }


def _serialize_salon(s) -> dict:
    if s is None:
        return None
    created_at = getattr(s, "created_at", None)
    created_at_iso = created_at.isoformat() if created_at is not None else None
    services = getattr(s, "services", None) or []
    return {
        "id": getattr(s, "id", None),
        "owner_id": getattr(s, "owner_id", None),
        "business_name": getattr(s, "business_name", None),
        "description": getattr(s, "description", None),
        "address": getattr(s, "address", None),
        "lat": getattr(s, "lat", None),
        "lng": getattr(s, "lng", None),
        "phone": getattr(s, "phone", None),
        "timezone": getattr(s, "timezone", None),
        "work_start_hour": getattr(s, "work_start_hour", None),
        "work_end_hour": getattr(s, "work_end_hour", None),
        "created_at": created_at_iso,
        "services": [_serialize_service(svc) for svc in services],
    }


# --- endpoints (create/list/get) ---

@router.post("", response_model=SalonOut, status_code=status.HTTP_201_CREATED)
def create_salon_endpoint(salon_in: SalonCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    # require Authorization header: "Bearer <token>"
    user = _get_user_from_auth_header(authorization, db)
    salon = create_salon(db, owner_id=user.id, salon_in=salon_in)
    return _serialize_salon(salon)


@router.get("", response_model=List[SalonOut])
def list_salons_endpoint(q: Optional[str] = Query(None), limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    salons = list_salons(db, q=q, limit=limit, offset=offset)
    # serialize each salon to plain dict
    return [_serialize_salon(s) for s in salons]


@router.get("/{salon_id}", response_model=SalonOut)
def get_salon_endpoint(salon_id: int, db: Session = Depends(get_db)):
    salon = get_salon(db, salon_id)
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Salon not found")
    return _serialize_salon(salon)


# --- Hours update endpoint ---

class SalonHoursUpdate(BaseModel):
    timezone: Optional[str] = Field(
        None, description="IANA timezone string, e.g. 'Asia/Kolkata'")
    work_start_hour: Optional[int] = Field(
        None, ge=0, le=23, description="Start hour in 24h (local salon tz)")
    work_end_hour: Optional[int] = Field(
        None, ge=0, le=23, description="End hour in 24h (local salon tz)")


@router.patch("/{salon_id}/hours")
def update_salon_hours(salon_id: int, payload: SalonHoursUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    Update salon timezone and simple working hours (single start/end hour per day).
    Only the salon owner or an admin may update.
    Returns the updated hours/timezone.
    """
    user = _get_user_from_auth_header(authorization, db)
    salon = get_salon(db, salon_id)
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Salon not found")

    # Authorization check: owner or admin
    if salon.owner_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # Apply updates (only fields provided)
    changed = False
    if payload.timezone is not None:
        salon.timezone = payload.timezone
        changed = True
    if payload.work_start_hour is not None:
        salon.work_start_hour = payload.work_start_hour
        changed = True
    if payload.work_end_hour is not None:
        salon.work_end_hour = payload.work_end_hour
        changed = True

    if changed:
        db.add(salon)
        db.commit()
        db.refresh(salon)

    # return the serialized salon (client-friendly)
    return _serialize_salon(salon)
