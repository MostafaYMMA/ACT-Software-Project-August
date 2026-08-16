from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from core.config import settings

bearer_scheme = HTTPBearer()


class CurrentPM:
    def __init__(self, pm_id: str, email: str):
        self.pm_id = pm_id
        self.email = email


def decode_supabase_jwt(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_pm(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentPM:
    payload = decode_supabase_jwt(credentials.credentials)
    pm_id = payload.get("sub")
    email = payload.get("email", "")
    if not pm_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim",
        )
    return CurrentPM(pm_id=pm_id, email=email)
