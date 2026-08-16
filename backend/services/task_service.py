from models.task import ParsedTaskRow, TaskStatus
from repositories import pm_repository, task_repository
from models.task import Task
from repositories import task_repository

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



def get_tasks_for_pm(pm_id: int) -> list[Task]:
    return [Task(**row) for row in task_repository.query_by_pm(pm_id)]