# app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://salon:lTss13uzfPYOgo0nqEceBkXr60YOWHfR@dpg-d58njs75r7bs738qtp90-a.virginia-postgres.render.com/salon_db_0czk")

# echo=True for SQL logging (handy while learning)
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
