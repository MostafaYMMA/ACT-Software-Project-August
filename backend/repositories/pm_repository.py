# backend/repositories/pm_repository.py
"""
Repositories are pure data access — no business decisions (that's services/).
"""
from repositories.supabase_client import get_supabase

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