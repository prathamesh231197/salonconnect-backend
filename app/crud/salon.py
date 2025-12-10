# app/crud/salon.py
from sqlalchemy.orm import Session
from db import models
from typing import List


def create_salon(db: Session, owner_id: int, salon_in) -> models.Salon:
    salon = models.Salon(
        owner_id=owner_id,
        business_name=salon_in.business_name,
        description=salon_in.description,
        address=salon_in.address,
        lat=salon_in.lat,
        lng=salon_in.lng,
        phone=salon_in.phone,
    )
    db.add(salon)
    db.flush()  # get salon.id

    # add services if provided
    for s in salon_in.services or []:
        service = models.Service(
            salon_id=salon.id,
            name=s.name,
            description=s.description,
            duration_minutes=s.duration_minutes,
            price=s.price
        )
        db.add(service)

    db.commit()
    db.refresh(salon)
    return salon


def get_salon(db: Session, salon_id: int) -> models.Salon:
    return db.query(models.Salon).filter(models.Salon.id == salon_id).first()


def list_salons(db: Session, q: str = None, limit: int = 20, offset: int = 0) -> List[models.Salon]:
    query = db.query(models.Salon)
    if q:
        q_like = f"%{q}%"
        query = query.filter(models.Salon.business_name.ilike(q_like))
    return query.order_by(models.Salon.id.desc()).offset(offset).limit(limit).all()
