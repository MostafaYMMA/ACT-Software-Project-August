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

def reassign_task(task_id: int, new_pm_id: int) -> dict | None:
    """Move a task to a different PM, regardless of its current status/owner.

    Unlike claim_task, this is not conditional on the task being unassigned -
    it's an admin override, so it always sets status back to 'assigned' under
    the new owner.
    """
    resp = (
        get_supabase()
        .table(TABLE)
        .update({"status": "assigned", "assigned_pm_id": new_pm_id})
        .eq("id", task_id)
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


def get_projects_rows(assigned_pm_id: int | None = None) -> list[dict]:
    """Fetch project_name, project_number, task_number, and pm, optionally filtered by assigned_pm_id."""
    supabase = get_supabase()
    query = supabase.table("tasks").select("project_name, project_number, task_number, pm")
    if assigned_pm_id is not None:
        query = query.eq("assigned_pm_id", assigned_pm_id)
    response = query.execute()
    return response.data    