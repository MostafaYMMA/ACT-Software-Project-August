# backend/services/auth_service.py
from fastapi import HTTPException

from models.auth import TokenResponse
from repositories import auth_repository, pm_repository


def login(email: str, password: str) -> TokenResponse:
    try:
        auth_response = auth_repository.sign_in(email, password)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid credentials") from exc

    session = auth_response.session
    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Login failed — check your credentials or confirm your email first",
        )

    pm_row = pm_repository.get_by_email(email)
    if pm_row is None or not pm_row.get("is_approved"):
        raise HTTPException(status_code=403, detail="Your account is still pending admin approval")

    return TokenResponse(access_token=session.access_token, refresh_token=session.refresh_token)