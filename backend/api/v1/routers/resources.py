from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependencies import get_current_pm
from models.pm import PM
from models.schedul import SupplierSchedule
from services import resource_service


router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[str])
def list_resources(
    current_pm: PM = Depends(get_current_pm),
) -> list[str]:
    """
    GET /api/v1/resources

    Return all unique resource names.
    """
    return resource_service.list_resources()


@router.get("/{resource_name}", response_model=list[SupplierSchedule])
def get_resource_details(
    resource_name: str,
    current_pm: PM = Depends(get_current_pm),
) -> list[SupplierSchedule]:
    """
    GET /api/v1/resources/{resource_name}

    Return every supplier_schedule row for the selected resource.
    """
    rows = resource_service.get_resource_details(resource_name)

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    return rows

@router.get("/filter", response_model=list[str])
def list_resources_by_attributes(
    brand: str | None = None,
    rate_type: str | None = None,
    project_country: str | None = None,
    remote_or_onsite: str | None = None,
    project_number: str | None = None,
    project_name: str | None = None,
    pm: str | None = None,
    resource_manager: str | None = None,
    current_pm: PM = Depends(get_current_pm),
) -> list[str]:
    """
    GET /api/v1/resources/filter?brand=...&rate_type=...
    All filters optional — combine any number. Returns distinct resource names.
    """
    attribute_filters = {
        "brand": brand, "rate_type": rate_type, "project_country": project_country,
        "remote_or_onsite": remote_or_onsite, "project_number": project_number,
        "project_name": project_name, "pm": pm, "resource_manager": resource_manager,
    }
    attribute_filters = {k: v for k, v in attribute_filters.items() if v is not None}

    return resource_service.list_resources_by_attributes(**attribute_filters)