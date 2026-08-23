# backend/api/v1/routers/auth.py
from fastapi import APIRouter

from models.auth import LoginRequest, TokenResponse
from services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    """POST /auth/login. Returns a JWT access token to send as
    Authorization: Bearer <token> on every other endpoint."""
    return auth_service.login(payload.email, payload.password)