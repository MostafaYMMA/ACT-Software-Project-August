# backend/repositories/schedule_repository.py
"""
Repositories are pure data access — no business decisions (that's services/).
"""
from repositories.supabase_client import get_supabase

TABLE = "supplier_schedule"  # confirm real table name


def get_hours_rows(**filters) -> list[dict]:
    """Fetch hours_allocated for rows matching any given filters."""
    supabase = get_supabase()
    query = supabase.table(TABLE).select("hours_allocated")
    for column, value in filters.items():
        if value is not None:
            query = query.eq(column, value)
    response = query.execute()
    return response.data

