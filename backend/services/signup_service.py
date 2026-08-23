# backend/services/signup_service.py
from fastapi import HTTPException

from models.signup import SignupRequest, SignupResponse
from repositories import pm_repository, signup_repository


def signup(payload: SignupRequest) -> SignupResponse:
    """Create a Supabase Auth user + a pending pms row.

    is_approved is always False here — the PM can't log in until an admin
    approves them (see the /pms/{pm_id}/approve endpoint).
    """
    existing = pm_repository.get_by_email(payload.email)
    if existing is not None:
        raise HTTPException(status_code=409, detail="A PM with this email already exists")

    try:
        auth_response = signup_repository.sign_up(payload.email, payload.password)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    auth_user = auth_response.user
    if auth_user is None:
        raise HTTPException(status_code=400, detail="Signup failed")

    username = payload.email.split("@")[0]

    pm_repository.create(
        {
            "email": payload.email,
            "auth_id": str(auth_user.id),
            "name": payload.name,
            "phone": payload.phone,
            "username": username,
            "is_admin": False,
            "is_approved": False,
        }
    )

    return SignupResponse(
        message="Your request has been sent. Please wait for admin approval before logging in."
    )