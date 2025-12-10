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


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
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
