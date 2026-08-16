from fastapi import APIRouter, Depends

from api.v1.dependencies import get_current_pm
from models.pm import PM
from services import email_service

router = APIRouter(prefix="/sync", tags=["sync"])


# TODO(open decision): whether this should be admin-only or callable by any
# authenticated PM. `get_current_pm` just requires a valid PM for now.
@router.post("/emails")
async def sync_emails(current_pm: PM = Depends(get_current_pm)):
    return await email_service.sync_new_emails()
