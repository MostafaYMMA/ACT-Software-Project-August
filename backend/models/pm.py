# backend/models/pm.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class PM(BaseModel):
    id: int
    email: str
    auth_id: UUID
    is_admin: bool = False
    name: Optional[str] = None
    username: Optional[str] = None
    created_at: Optional[datetime] = None

class PMCreate(BaseModel):
    """Payload for admin-only PM creation. auth_id is required because PM
    accounts are provisioned by the dev team's seed script (Supabase Auth
    user must already exist) — this endpoint only inserts the pms row."""
    email: str
    auth_id: str
    name: Optional[str] = None
    is_admin: bool = False
    username: str
    

class PMAdminUpdate(BaseModel):
    """Payload for admin-only promote/demote. is_admin defaults to True so a
    plain {} body on the "promote" endpoint does the expected thing."""
    is_admin: bool = True






PM.model_rebuild()
PMCreate.model_rebuild()
PMAdminUpdate.model_rebuild()
