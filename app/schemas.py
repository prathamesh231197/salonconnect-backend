# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None

# --- Salon / Service schemas ---


class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price: float


class ServiceOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price: float

    class Config:
        from_attributes = True


class SalonCreate(BaseModel):
    business_name: str
    description: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    phone: Optional[str] = None
    services: Optional[List[ServiceCreate]] = []


class SalonOut(BaseModel):
    id: int
    owner_id: int
    business_name: str
    description: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    phone: Optional[str] = None
    services: List[ServiceOut] = []

    class Config:
        from_attributes = True


# bookings schemas (add to app/schemas.py)

class BookingCreate(BaseModel):
    salon_id: int
    service_id: int
    start_time: datetime  # ISO format accepted
    # end_time optional if you want to compute from service duration; include for flexibility:
    end_time: Optional[datetime] = None


class BookingOut(BaseModel):
    id: int
    salon_id: int
    service_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
