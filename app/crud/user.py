# app/crud/user.py
from sqlalchemy.orm import Session
from db import models
from passlib.context import CryptContext
from fastapi import HTTPException, status

# pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
# Use PBKDF2-SHA256 to avoid issues with bcrypt native libs inside the container.
# PBKDF2 is secure and works great for development. For production consider Argon2.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
BCRYPT_MAX_BYTES = 72


def _ensure_password_ok(password: str):
    if password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password required")
    # check encoded byte length (bcrypt limit is bytes, not characters)
    if len(password.encode("utf-8")) > BCRYPT_MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password too long. Maximum {BCRYPT_MAX_BYTES} bytes (usually ~72 ASCII characters)."
        )


def _normalize_for_hash(password: str) -> str:
    """
    Optionally normalize/truncate before hashing.
    Here we only validate length (reject too-long). If you prefer truncation,
    replace this function to truncate to BCRYPT_MAX_BYTES bytes.
    """
    _ensure_password_ok(password)
    return password


def get_user_by_email(db: Session, email: str):
    """Return a User by email or None"""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, *, email: str, password: str, name: str = None, phone: str = None, role: int = None):
    """Create and return a new User"""
    # validate password length before hashing
    normalized = _normalize_for_hash(password)
    hashed = pwd_context.hash(normalized)
    user = models.User(email=email, hashed_password=hashed,
                       name=name, phone=phone, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against stored hash"""
    # also validate length on verify side to avoid passlib raising
    _ensure_password_ok(plain_password)
    return pwd_context.verify(plain_password, hashed_password)
