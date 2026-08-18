"""
Repositories are pure data access — no business decisions (that's services/).
"""
from repositories.supabase_client import get_supabase

TABLE = "tasks"


def list_tasks() -> list[dict]:
    resp = get_supabase().table(TABLE).select("*").execute()
    return resp.data


def get_task_by_id(task_id: int) -> dict | None:
    resp = get_supabase().table(TABLE).select("*").eq("id", task_id).maybe_single().execute()
    return resp.data if resp else None


def find_by_source_reference(source_reference: str) -> dict | None:
    """Look up an existing task by the (not-yet-finalized) dedupe key.

    See CLAUDE.md "Open decisions" - source_reference is a placeholder until
    the team confirms which field(s) uniquely identify a task record.
    """
    resp = (
        get_supabase()
        .table(TABLE)
        .select("*")
        .eq("source_reference", source_reference)
        .maybe_single()
        .execute()
    )
    return resp.data if resp else None


def create_task(task: dict) -> dict:
    resp = get_supabase().table(TABLE).insert(task).execute()
    return resp.data[0]


def overwrite_task(task_id: int, task: dict) -> dict:
    """Fully replace an existing task record (not a merge), per CLAUDE.md rule 3."""
    resp = get_supabase().table(TABLE).update(task).eq("id", task_id).execute()
    return resp.data[0]


def delete_task(task_id: int) -> bool:
    """Permanently remove a task record."""
    resp = get_supabase().table(TABLE).delete().eq("id", task_id).execute()
    return bool(resp.data)


def unassign_task(task_id: int) -> dict | None:
    """Clear a task's assignment and set it back to unassigned."""
    resp = (
        get_supabase()
        .table(TABLE)
        .update({"status": "unassigned", "assigned_pm_id": None})
        .eq("id", task_id)
        .execute()
    )
    return resp.data[0] if resp.data else None


def claim_task(task_id: int, pm_id: int) -> dict | None:
    """Atomically self-assign an unassigned task.

    Uses a conditional UPDATE ... WHERE status = 'unassigned' so two PMs
    racing to claim the same task cannot both succeed (CLAUDE.md convention -
    no application-level locking).
    """
    resp = (
        get_supabase()
        .table(TABLE)
        .update({"status": "assigned", "assigned_pm_id": pm_id})
        .eq("id", task_id)
        .eq("status", "unassigned")
        .execute()
    )
    return resp.data[0] if resp.data else None

def query_by_pm(pm_id: int) -> list[dict]:
    """Fetch all tasks assigned to a specific PM."""
    supabase = get_supabase()
    response = (
        supabase.table("tasks")
        .select("*")
        .eq("assigned_pm_id", pm_id)
        .execute()
    )
    return response.data


def search_tasks(
    search_query: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    status: str | None = None,
) -> list[dict]:
    """
    Search and filter tasks by text query and date range.
    
    Args:
        search_query: Text to search in title, description, source_reference
        from_date: ISO format date string (YYYY-MM-DD) for start of range
        to_date: ISO format date string (YYYY-MM-DD) for end of range
        status: Filter by status ('assigned' or 'unassigned')
    
    Returns:
        List of matching tasks.
    """
    supabase = get_supabase()
    query = supabase.table(TABLE).select("*")
    
    # Apply status filter if provided
    if status:
        query = query.eq("status", status)
    
    # Apply date filters if provided
    if from_date:
        query = query.gte("created_at", f"{from_date}T00:00:00Z")
    if to_date:
        query = query.lte("created_at", f"{to_date}T23:59:59Z")
    
    resp = query.execute()
    tasks = resp.data if resp.data else []
    
    # Apply text search filter if provided (client-side since Supabase
    # basic API doesn't have full-text search built in for all fields)
    if search_query:
        search_lower = search_query.lower()
        tasks = [
            t for t in tasks
            if (
                search_lower in (t.get("title") or "").lower()
                or search_lower in (t.get("description") or "").lower()
                or search_lower in (t.get("source_reference") or "").lower()
            )
        ]
    
    return tasks