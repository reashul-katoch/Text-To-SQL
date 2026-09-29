from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    username: str
    password: str


# Temporary users
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "analyst": {
        "password": "analyst123",
        "role": "analyst"
    },
    "viewer": {
        "password": "viewer123",
        "role": "viewer"
    }
}


@router.post("/login")
def login(request: LoginRequest):

    user = USERS.get(request.username)

    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token({
        "sub": request.username,
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }