# app/api/v1/users.py
from fastapi import APIRouter, Depends

from api.deps import get_current_user

router = APIRouter()


@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    # return subset of fields (avoid returning hashed_password)
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "phone": current_user.phone,
        "role": current_user.role,
        "created_at": str(current_user.created_at),
    }
