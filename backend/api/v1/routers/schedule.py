# backend/api/v1/routers/schedule.py
from fastapi import APIRouter
from services import schedule_service

router = APIRouter(prefix="/schedule", tags=["schedule"])


# backend/api/v1/routers/schedule.py

@router.get("/hours/dynamic")
def get_hours_dynamic(
    resource: str,
    brand: str | None = None,
    rate_type: str | None = None,
    project_country: str | None = None,
    remote_or_onsite: str | None = None,
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
        "remote_or_onsite": remote_or_onsite,
        "project_number": project_number,
        "project_name": project_name,
        "pm": pm,
        "resource_manager": resource_manager,
    }
    attribute_filters = {k: v for k, v in attribute_filters.items() if v is not None}

    return schedule_service.get_total_hours_dynamic(resource, **attribute_filters)