# backend/api/v1/routers/pms.py

from fastapi import APIRouter
from models.pm import PM
from services import pm_service

router = APIRouter(prefix="/pms", tags=["pms"])


@router.get("/", response_model=list[PM])
def list_pms():
    """GET /pms — return every PM."""
    return pm_service.list_pms()


@router.get("/{pm_id}", response_model=PM)
def get_pm(pm_id: int):
    """GET /pms/{pm_id} — return one PM by id."""
    return pm_service.get_pm(pm_id)