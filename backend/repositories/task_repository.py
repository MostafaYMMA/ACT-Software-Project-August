"""
Example of the pattern to copy for pm_repository.py and sync_state_repository.py.
Repositories are pure data access — no business decisions (that's services/).
"""

from repositories.supabase_client import get_supabase

TABLE = "tasks"


def list_tasks() -> list[dict]:
    supabase = get_supabase()
    response = supabase.table(TABLE).select("*").execute()
    return response.data


def get_task_by_id(task_id: str) -> dict | None:
    supabase = get_supabase()
    response = supabase.table(TABLE).select("*").eq("id", task_id).maybe_single().execute()
    return response.data if response else None


def create_task(task: dict) -> dict:
    supabase = get_supabase()
    response = supabase.table(TABLE).insert(task).execute()
    return response.data[0]


def overwrite_task(match_column: str, match_value: str, task: dict) -> dict:
    """
    Full overwrite of an existing task record (per CLAUDE.md rule 3 — not a merge).
    `match_column` is whatever field the team decides is the dedupe key
    (still an open decision as of writing).
    """
    supabase = get_supabase()
    response = (
        supabase.table(TABLE).update(task).eq(match_column, match_value).execute()
    )
    return response.data[0]


def claim_task_if_unassigned(task_id: str, pm_id: str) -> dict | None:
    """
    Atomic conditional update for the self-assign race condition:
    only succeeds if status is still 'unassigned' at update time.
    """
    supabase = get_supabase()
    response = (
        supabase.table(TABLE)
        .update({"status": "assigned", "assigned_pm_id": pm_id})
        .eq("id", task_id)
        .eq("status", "unassigned")
        .execute()
    )
    return response.data[0] if response.data else None