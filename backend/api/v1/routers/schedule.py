# backend/api/v1/routers/schedule.py
from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependencies import get_current_pm
from models.pm import PM
from models.schedul import ProjectStatusUpdate
from services import schedule_service

router = APIRouter(prefix="/schedule", tags=["schedule"])


# backend/api/v1/routers/schedule.py

@router.get("/hours/dynamic")
def get_hours_dynamic(
    resource: str,
    brand: str | None = None,
    rate_type: str | None = None,
    project_country: str | None = None,
    remote_onsite: str | None = None,
    project_number: str | None = None,
    project_name: str | None = None,
    pm: str | None = None,
    resource_manager: str | None = None,
) -> float:
    """
    GET /schedule/hours/dynamic?resource=...&brand=...&rate_type=...
    All attribute filters optional — combine any number.
    """
    attribute_filters = {
        "brand": brand,
        "rate_type": rate_type,
        "project_country": project_country,
        "remote_onsite": remote_onsite,
        "project_number": project_number,
        "project_name": project_name,
        "pm": pm,
        "resource_manager": resource_manager,
    }
    attribute_filters = {k: v for k, v in attribute_filters.items() if v is not None}

    return schedule_service.get_total_hours_dynamic(resource, **attribute_filters)

@router.patch("/projects/{project_number}/status")
def update_project_status(
    project_number: str,
    body: ProjectStatusUpdate,
    current_pm: PM = Depends(get_current_pm),
) -> list[dict]:
    """
    PATCH /schedule/projects/{project_number}/status
    body: {"project_status": "Active" | "Post-WAR" | "Pending" | "Not-Active"}

    A PM can only change the status of a project where the `pm` column on
    its supplier_schedule rows matches their own name. Admins can update any
    project.
    """
    try:
        return schedule_service.update_project_status(
            project_number, current_pm, body.project_status.value
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))