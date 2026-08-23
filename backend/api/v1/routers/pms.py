# backend/api/v1/routers/pms.py

from fastapi import APIRouter, Depends

from api.v1.dependencies import get_current_pm, require_admin
from models.pm import PM, PMCreate, PMAdminUpdate
from services import pm_service

router = APIRouter(prefix="/pms", tags=["pms"])


@router.get("/", response_model=list[PM])
def list_pms(current_pm: PM = Depends(get_current_pm)):
    """GET /pms — return every PM."""
    return pm_service.list_pms()


@router.get("/pending", response_model=list[PM])
def get_pending_pms(current_pm: PM = Depends(require_admin)):
    """GET /pms/pending — admin-only. List every PM still waiting for
    approval (id, name, email, etc.)."""
    return pm_service.list_pending_pms()


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


@router.patch("/{pm_id}/admin", response_model=PM)
def set_admin_status(
    pm_id: int,
    payload: PMAdminUpdate,
    current_pm: PM = Depends(require_admin),
):
    """PATCH /pms/{pm_id}/admin — admin-only. Promote (is_admin: true, the
    default) or demote (is_admin: false) an existing PM."""
    return pm_service.set_admin_status(pm_id, payload.is_admin, current_pm)


@router.post("/heartbeat")
def heartbeat(current_pm: PM = Depends(get_current_pm)):
    pm_service.record_heartbeat(current_pm.id)
    return {"status": "ok"}


@router.get("/{pm_id}/online")
def check_online(pm_id: int) -> bool:
    return pm_service.is_online(pm_id)


@router.patch("/{pm_id}/approve", response_model=PM)
def approve_pm(pm_id: int, current_pm: PM = Depends(require_admin)):
    """PATCH /pms/{pm_id}/approve — admin-only. Approve a pending signup."""
    return pm_service.approve_pm(pm_id, current_pm)