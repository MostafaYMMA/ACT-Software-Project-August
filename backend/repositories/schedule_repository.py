# backend/repositories/schedule_repository.py
"""
Repositories are pure data access — no business decisions (that's services/).
"""
from repositories.supabase_client import get_supabase

TABLE = "tasks"  # confirm real table name


def get_hours_rows(**filters) -> list[dict]:
    """Fetch hours_allocated for rows matching any given filters."""
    supabase = get_supabase()
    query = supabase.table(TABLE).select("hours_allocated")
    for column, value in filters.items():
        if value is not None:
            query = query.eq(column, value)
    response = query.execute()
    return response.data

def get_rows_by_project_number(project_number: str) -> list[dict]:
    supabase = get_supabase()
    response = (
        supabase.table(TABLE).select("*").eq("project_number", project_number).execute()
    )
    return response.data or []


def update_project_status(project_number: str, new_status: str, pm_name: str | None = None) -> list[dict]:
    supabase = get_supabase()
    query = supabase.table(TABLE).update({"project_status": new_status}).eq(
        "project_number", project_number
    )
    if pm_name is not None:
        query = query.eq("pm", pm_name)
    response = query.execute()
    return response.data or []