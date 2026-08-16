# backend/api/v1/routers/pms.py

from fastapi import APIRouter, Depends

from api.v1.dependencies import get_current_pm
from models.pm import PM
from services import pm_service

router = APIRouter(prefix="/pms", tags=["pms"])


@router.get("/", response_model=list[PM])
def list_pms(current_pm: PM = Depends(get_current_pm)):
    """GET /pms — return every PM."""
    return pm_service.list_pms()


@router.get("/{pm_id}", response_model=PM)
def get_pm(pm_id: int, current_pm: PM = Depends(get_current_pm)):
    """GET /pms/{pm_id} — return one PM by id."""
    return pm_service.get_pm(pm_id)
