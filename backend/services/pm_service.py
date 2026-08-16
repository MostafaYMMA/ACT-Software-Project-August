# backend/services/pm_service.py

from fastapi import HTTPException
from models.pm import PM
from repositories import pm_repository


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