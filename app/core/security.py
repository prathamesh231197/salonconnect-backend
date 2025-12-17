# app/core/security.py
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt


SECRET_KEY = os.getenv(
    "SECRET_KEY", "please_change_this_to_a_random_secret_in_prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


from typing import Union, Dict, Any

def create_access_token(subject: Union[str, Dict[str, Any]], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT. `subject` can be an email string, a dict, or a SQLAlchemy user object.
    If a user dict/object is provided, include a sanitized `user` claim (excluding password/hash).
    """
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    user_claim = None
    # If subject is a string, treat as email
    if isinstance(subject, str):
        sub = subject
    else:
        # If it's a dict (or sqlalchemy model-like), build a sanitized user dict
        if isinstance(subject, dict):
            sub = str(subject.get("email")) if subject.get("email") else str(subject)
            user_claim = {k: v for k, v in subject.items() if k not in ("hashed_password", "password")}
        else:
            # likely a SQLAlchemy model instance
            sub = getattr(subject, "email", str(subject))
            user_claim = {
                "id": getattr(subject, "id", None),
                "email": getattr(subject, "email", None),
                "name": getattr(subject, "name", None),
                "phone": getattr(subject, "phone", None),
                "role": getattr(subject, "role", None),
                "created_at": str(getattr(subject, "created_at")) if getattr(subject, "created_at", None) else None,
            }

    to_encode = {"exp": expire, "sub": sub}
    if user_claim:
        to_encode["user"] = user_claim

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# existing constants: SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def decode_access_token(token: str) -> Optional[str]:
    """
    Decode JWT and return the subject (email) or None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
