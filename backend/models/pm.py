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
