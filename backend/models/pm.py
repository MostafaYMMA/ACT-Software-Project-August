# backend/models/pm.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PM(BaseModel):
    id: int
    email: str
    auth_id: str          # links this PM row to their Supabase Auth login
    is_admin: bool = False          # ← new field
    name: Optional[str] = None
    created_at: Optional[datetime] = None

class PMCreate(BaseModel):
    """Payload for admin-only PM creation. auth_id is required because PM
    accounts are provisioned by the dev team's seed script (Supabase Auth
    user must already exist) — this endpoint only inserts the pms row."""
    email: str
    auth_id: str
    name: Optional[str] = None
    is_admin: bool = False