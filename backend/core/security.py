# core/security.py
from functools import lru_cache

import jwt
from fastapi import HTTPException, status
from core.config import settings

# Supabase projects created after the asymmetric-keys rollout sign JWTs with
# ES256 (or RS256) using a rotating keypair, not the legacy HS256 shared
# secret - so verification has to fetch Supabase's public JWKS instead of
# using settings.supabase_jwt_secret directly.
_JWKS_URL = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"


@lru_cache
def _jwk_client() -> jwt.PyJWKClient:
    return jwt.PyJWKClient(_JWKS_URL)


def verify_jwt(token: str) -> dict:
    """Verify a Supabase JWT and return its decoded payload."""
    try:
        signing_key = _jwk_client().get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except (jwt.InvalidTokenError, jwt.PyJWKClientError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_auth_id(payload: dict) -> str:
    """Extract the Supabase user id (auth_id) from a verified JWT payload."""
    auth_id = payload.get("sub")
    if not auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")
    return auth_id
