# backend/api/v1/routers/signup.py
from fastapi import APIRouter

from models.signup import SignupRequest, SignupResponse
from services import signup_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=SignupResponse, status_code=201)
def signup(payload: SignupRequest):
    """POST /auth/signup — self-service signup. Creates a Supabase Auth user
    + a pending pms row. Login stays blocked until an admin approves it."""
    return signup_service.signup(payload)