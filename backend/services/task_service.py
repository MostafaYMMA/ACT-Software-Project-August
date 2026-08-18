from models.task import ParsedTaskRow, TaskStatus,Task
from repositories import pm_repository, task_repository


def upsert_task_from_row(row: ParsedTaskRow, source_email_id: str) -> dict:
    """Apply the create-vs-overwrite / assigned-vs-unassigned rules from CLAUDE.md.

    - No PM specified -> status: unassigned, any PM can self-claim later.
    - PM specified -> status: assigned to that PM.
    - Row references an existing task (matched via source_reference) ->
      fully overwrite the existing record, not a merge.
    """
    assigned_pm_id = None
    status = TaskStatus.UNASSIGNED
    if row.assigned_pm_email:
        pm = pm_repository.get_by_email(row.assigned_pm_email)
        if pm:
            assigned_pm_id = pm["id"]
            status = TaskStatus.ASSIGNED

    task_payload = {
        "title": row.title,
        "description": row.description,
        "status": status.value,
        "assigned_pm_id": assigned_pm_id,
        "source_email_id": source_email_id,
        "source_reference": row.source_reference,
    }

    existing = (
        task_repository.find_by_source_reference(row.source_reference)
        if row.source_reference
        else None
    )
    if existing:
        return task_repository.overwrite_task(existing["id"], task_payload)
    return task_repository.create_task(task_payload)


def list_tasks() -> list[dict]:
    return task_repository.list_tasks()


def get_task(task_id: int) -> dict | None:
    return task_repository.get_task_by_id(task_id)


def claim_task(task_id: int, pm_id: int) -> dict:
    """Self-assign an unassigned task. Relies on an atomic conditional UPDATE
    in the repository layer to resolve the two-PMs-claiming-at-once race."""
    claimed = task_repository.claim_task(task_id, pm_id)
    if claimed is None:
        raise ValueError("Task is not claimable (already assigned or does not exist)")
    return claimed


def delete_task(task_id: int) -> None:
    """Permanently delete a task. Caller (router) must enforce admin-only access."""
    task = task_repository.get_task_by_id(task_id)
    if task is None:
        raise ValueError("Task not found")
    task_repository.delete_task(task_id)


def unassign_task(task_id: int, current_pm) -> dict:
    """Unassign a task. Allowed for the PM it's currently assigned to, or an admin."""
    task = task_repository.get_task_by_id(task_id)
    if task is None:
        raise ValueError("Task not found")

    if not current_pm.is_admin and task.get("assigned_pm_id") != current_pm.id:
        raise PermissionError("You can only unassign tasks assigned to you")

    updated = task_repository.unassign_task(task_id)
    if updated is None:
        raise ValueError("Task could not be unassigned")
    return updated

def get_tasks_for_pm(pm_id: int) -> list[Task]:
    """Get all tasks belonging to a specific PM."""
    return [Task(**row) for row in task_repository.query_by_pm(pm_id)]


def search_tasks(
    search_query: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    status: str | None = None,
) -> list[dict]:
    """
    Search tasks by text and date range.
    
    Args:
        search_query: Text to search in task fields
        from_date: ISO format date (YYYY-MM-DD)
        to_date: ISO format date (YYYY-MM-DD)
        status: Filter by status (assigned/unassigned)
    
    Returns:
        List of matching tasks.
    """
    return task_repository.search_tasks(search_query, from_date, to_date, status)