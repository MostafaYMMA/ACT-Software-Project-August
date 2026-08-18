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