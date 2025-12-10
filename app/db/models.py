# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from db.session import Base

# --- User model (single definition) ---


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="customer")  # customer | barber | admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# --- Salon model ---


class Salon(Base):
    __tablename__ = "salons"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", backref="salons")
    services = relationship(
        "Service", back_populates="salon", cascade="all, delete-orphan")

# --- Service model ---


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False, default=30)
    price = Column(Float, nullable=False, default=0.0)

    salon = relationship("Salon", back_populates="services")
