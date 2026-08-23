# backend/repositories/pm_repository.py
"""
Repositories are pure data access — no business decisions (that's services/).
"""
from repositories.supabase_client import get_supabase
from datetime import datetime, timezone
 
TABLE = "pms"


def get_by_id(pm_id: int) -> dict | None:
    """Fetch a single PM by their database id."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("id", pm_id)
        .maybe_single()
        .execute()
    )
    return response.data if response else None


def get_by_email(email: str) -> dict | None:
    """Fetch a single PM by their email."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("email", email)
        .maybe_single()
        .execute()
    )
    return response.data if response else None


def get_by_auth_id(auth_id: str) -> dict | None:
    """Fetch a single PM by their Supabase Auth id."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("auth_id", auth_id)
        .maybe_single()
        .execute()
    )
    return response.data if response else None


def list_all() -> list[dict]:
    """Fetch every PM in the database."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .select("*")
        .execute()
    )
    return response.data


def create(pm_data: dict) -> dict:
    """Insert a new PM row. Pure data access — no business rules here."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .insert(pm_data)
        .execute()
    )
    return response.data[0]


def update_last_seen(pm_id: int) -> None:
    supabase = get_supabase()
    supabase.table(TABLE).update(
        {"last_seen": datetime.now(timezone.utc).isoformat()}
    ).eq("id", pm_id).execute()


def update(pm_id: int, fields: dict) -> dict | None:
    """Update arbitrary columns on a PM row (e.g. {'is_admin': True}).

    Pure data access — the decision of *whether* someone is allowed to make
    this change belongs in services/pm_service.py, not here.
    """
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .update(fields)
        .eq("id", pm_id)
        .execute()
    )
    return response.data[0] if response.data else None
 
def list_pending() -> list[dict]:
    """Fetch every PM row where is_approved is false."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("is_approved", False)
        .execute()
    )
    return response.data or []
