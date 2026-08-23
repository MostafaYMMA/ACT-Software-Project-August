from fastapi import APIRouter, Depends

from api.v1.dependencies import require_admin
from models.pm import PM
from services import email_service

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/emails")
async def sync_emails(current_pm: PM = Depends(require_admin)):
    return await email_service.sync_new_emails()
