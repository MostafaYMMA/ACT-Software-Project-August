
"""
Pure data access for resources stored in supplier_schedule.
No business logic belongs in this file.
"""

from repositories.supabase_client import get_supabase


TABLE = "supplier_schedule"


def list_resource_rows() -> list[dict]:
    """
    Fetch the resource column.

    Removing duplicates and empty values is handled by the service layer.
    """
    response = (
        get_supabase()
        .table(TABLE)
        .select("resource")
        .order("resource")
        .execute()
    )
    return response.data or []


def get_rows_by_resource(resource_name: str) -> list[dict]:
    """Fetch every supplier_schedule row belonging to one resource."""
    response = (
        get_supabase()
        .table(TABLE)
        .select("*")
        .eq("resource", resource_name)
        .order("resource_start")
        .execute()
    )
    return response.data or []