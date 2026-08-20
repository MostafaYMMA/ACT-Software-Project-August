# api/v1/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_jwt, get_auth_id
from repositories.pm_repository import get_by_auth_id
from models.pm import PM

# OAuth2PasswordBearer (rather than plain HTTPBearer) is what makes Swagger's
# "Authorize" button render a username/password login form instead of a raw
# token field. It still just reads the same `Authorization: Bearer <token>`
# header under the hood — tokenUrl only tells Swagger which endpoint to POST
# the login form to (see /dev/login in main.py).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="dev/login")

async def get_current_pm(
    token: str = Depends(oauth2_scheme),
) -> PM:
    payload = verify_jwt(token)
    auth_id = get_auth_id(payload)

    # get_by_auth_id is sync (Mohamed's pm_repository.py) and returns a raw dict.
    pm_row = get_by_auth_id(auth_id)
    if pm_row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PM not found")
    # TODO(Adam): confirm PM field names against Mohamed's real models/pm.py (esp. admin flag).
    return PM(**pm_row)

async def require_admin(pm: PM = Depends(get_current_pm)) -> PM:
    if not pm.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return pm
