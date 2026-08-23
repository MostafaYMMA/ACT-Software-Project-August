# backend/services/pm_service.py

from fastapi import HTTPException
from models.pm import PM
from repositories import pm_repository
from datetime import datetime, timezone, timedelta


def get_pm(pm_id: int) -> PM:
    """Get a single PM by id, or raise a 404 if they don't exist."""
    pm = pm_repository.get_by_id(pm_id)

    if pm is None:
        raise HTTPException(status_code=404, detail="PM not found")

    return PM(**pm)


def list_pms() -> list[PM]:
    """Get every PM."""
    return [PM(**row) for row in pm_repository.list_all()]


def get_by_email(pm_email: str) -> PM:
    """Get a single PM by email, or raise a 404 if they don't exist."""
    pm = pm_repository.get_by_email(pm_email)

    if pm is None:
        raise HTTPException(status_code=404, detail="PM not found")

    return PM(**pm)

def get_by_auth_id(auth_id: str) -> PM:
    """Get a single PM by their Supabase Auth id, or raise a 404 if they don't exist."""
    pm = pm_repository.get_by_auth_id(auth_id)

    if pm is None:
        raise HTTPException(status_code=404, detail="PM not found")

    return PM(**pm)


from models.pm import PMCreate  # add to the existing "from models.pm import PM" line instead

def create_pm(new_pm: PMCreate, requesting_pm: PM) -> PM:
    """Admin-only: create a new PM record."""
    if not requesting_pm.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    existing = pm_repository.get_by_email(new_pm.email)
    if existing is not None:
        raise HTTPException(status_code=409, detail="A PM with this email already exists")

    created = pm_repository.create(new_pm.model_dump())
    return PM(**created)

def set_admin_status(pm_id: int, is_admin: bool, requesting_pm: PM) -> PM:
    """Admin-only: promote a PM to admin, or demote them back to a regular PM.

    Used for both "promote user" (is_admin=True) and, symmetrically, revoking
    admin rights (is_admin=False) — same rule, same guard rails.
    """
    if not requesting_pm.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    target = pm_repository.get_by_id(pm_id)
    if target is None:
        raise HTTPException(status_code=404, detail="PM not found")

    # Don't let the last admin accidentally demote themselves and lock
    # everyone out of admin-only endpoints.
    if pm_id == requesting_pm.id and not is_admin:
        raise HTTPException(status_code=400, detail="You cannot remove your own admin access")

    updated = pm_repository.update(pm_id, {"is_admin": is_admin})
    if updated is None:
        raise HTTPException(status_code=404, detail="PM not found")

    return PM(**updated)

def approve_pm(pm_id: int, requesting_pm: PM) -> PM:
    """Admin-only: approve a pending signup so the PM can log in."""
    if not requesting_pm.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    target = pm_repository.get_by_id(pm_id)
    if target is None:
        raise HTTPException(status_code=404, detail="PM not found")

    updated = pm_repository.update(pm_id, {"is_approved": True})
    if updated is None:
        raise HTTPException(status_code=404, detail="PM not found")

    return PM(**updated)

def record_heartbeat(pm_id: int) -> None:
    pm_repository.update_last_seen(pm_id)


def is_online(pm_id: int) -> bool:
    pm = pm_repository.get_by_id(pm_id)
    if pm is None or pm.get("last_seen") is None:
        return False
    last_seen = datetime.fromisoformat(pm["last_seen"])
    return datetime.now(timezone.utc) - last_seen < timedelta(seconds=60)
