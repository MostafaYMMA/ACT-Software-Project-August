# backend/api/v1/routers/pms.py

from fastapi import APIRouter, Depends

from api.v1.dependencies import get_current_pm, require_admin
from models.pm import PM, PMCreate
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



@router.post("/", response_model=PM, status_code=201)
def add_pm(new_pm: PMCreate, current_pm: PM = Depends(require_admin)):
    """POST /pms — admin-only. Creates a new PM record.

    Note: this only inserts the pms row. The Supabase Auth user (auth_id)
    must already exist — that's provisioned separately by the seed script.
    """
    return pm_service.create_pm(new_pm, current_pm)