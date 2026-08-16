# core/security.py
import jwt
from fastapi import HTTPException, status
from core.config import settings

def verify_jwt(token: str) -> dict:
    """Verify a Supabase JWT and return its decoded payload."""
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_auth_id(payload: dict) -> str:
    """Extract the Supabase user id (auth_id) from a verified JWT payload."""
    auth_id = payload.get("sub")
    if not auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")
    return auth_id