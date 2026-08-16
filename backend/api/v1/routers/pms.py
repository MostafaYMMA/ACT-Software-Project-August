from fastapi import APIRouter, Depends

from api.v1.dependencies import CurrentPM, get_current_pm
from services import pm_service

router = APIRouter(prefix="/pms", tags=["pms"])


@router.get("")
def list_pms(current_pm: CurrentPM = Depends(get_current_pm)):
    return pm_service.list_pms()
