from datetime import datetime, timezone

from models.task import ParsedTaskRow, TaskStatus
from repositories import pm_repository, task_repository
from datetime import datetime,date

# Days-until-deadline thresholds for the derived "priority" label - tuned
# for a PM checking their list once a day, not a real-time queue.
_URGENT_WITHIN_DAYS = 1
_HIGH_WITHIN_DAYS = 3
_MEDIUM_WITHIN_DAYS = 7


def _deadline_timestamp(task: dict) -> float | None:
    """Effective end date used for prioritization.

    Email-sourced tasks carry `due_date`; supplier-schedule (Excel) rows
    instead carry `resource_end` (see services/parser.py). Whichever is
    present is the task's deadline for this purpose.
    """
    raw = task.get("due_date") or task.get("resource_end")
    if not raw:
        return None
    dt = raw if isinstance(raw, datetime) else datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def _priority_label(deadline_ts: float | None) -> str:
    """Derived priority: how soon a task's deadline is, not a stored field.

    No deadline -> lowest priority, since there's nothing to be urgent about.
    """
    if deadline_ts is None:
        return "low"
    days_until = (deadline_ts - datetime.now(timezone.utc).timestamp()) / 86400
    if days_until <= _URGENT_WITHIN_DAYS:
        return "urgent"
    if days_until <= _HIGH_WITHIN_DAYS:
        return "high"
    if days_until <= _MEDIUM_WITHIN_DAYS:
        return "medium"
    return "low"


def _sorted_by_priority(tasks: list[dict]) -> list[dict]:
    """Order tasks so the ones ending soonest surface first, tagging each
    with a derived `priority` label. Tasks with no known deadline sort last.
    """
    decorated = []
    for task in tasks:
        deadline_ts = _deadline_timestamp(task)
        decorated.append((deadline_ts, {**task, "priority": _priority_label(deadline_ts)}))

    decorated.sort(key=lambda pair: (pair[0] is None, pair[0]))
    return [task for _, task in decorated]


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
        "due_date": row.due_date.isoformat() if row.due_date else None,
    }

    existing = (
        task_repository.find_by_source_reference(row.source_reference)
        if row.source_reference
        else None
    )
    if existing:
        return task_repository.overwrite_task(existing["id"], task_payload)
    return task_repository.create_task(task_payload)


def upsert_supplier_schedule_row(row: dict, source_email_id: str) -> dict:
    """Apply one parsed Excel row (see services/parser.parse_excel_to_task_rows)
    to the `tasks` table.

    The table's primary key is (project_name, project_number, task_number) -
    a row with the same key fully overwrites the existing record (not a
    merge), including re-resolving assigned_pm_id/status from the new `pm`
    value, since a changed PM is the most common kind of update expected.
    """
    assigned_pm_id = None
    status = TaskStatus.UNASSIGNED
    pm_email = row.get("pm")
    if pm_email:
        pm = pm_repository.get_by_email(pm_email)
        if pm:
            assigned_pm_id = pm["id"]
            status = TaskStatus.ASSIGNED

    payload = {
        **row,
        "assigned_pm_id": assigned_pm_id,
        "status": status.value,
        "source_email_id": source_email_id,
    }
    return task_repository.upsert_task(payload)


def list_tasks() -> list[dict]:
    """All tasks, highest priority (soonest deadline) first."""
    return _sorted_by_priority(task_repository.list_tasks())


def get_task(task_id: int) -> dict | None:
    task = task_repository.get_task_by_id(task_id)
    if task is None:
        return None
    return {**task, "priority": _priority_label(_deadline_timestamp(task))}


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

def reassign_task(task_id: int, new_pm_id: int, current_pm) -> dict:
    """Admin-only: move a task to a different PM, no matter who (if anyone)
    currently holds it. Router must enforce admin access via require_admin;
    this function re-checks so the rule holds even if it's ever called from
    somewhere else.
    """
    if not current_pm.is_admin:
        raise PermissionError("Only an admin can transfer a task between PMs")

    task = task_repository.get_task_by_id(task_id)
    if task is None:
        raise ValueError("Task not found")

    new_pm = pm_repository.get_by_id(new_pm_id)
    if new_pm is None:
        raise ValueError("Target PM not found")

    updated = task_repository.reassign_task(task_id, new_pm_id, new_pm["name"])
    if updated is None:
        raise ValueError("Task could not be reassigned")
    return updated


def get_tasks_for_pm(pm_id: int) -> list[dict]:
    """All tasks belonging to a specific PM, highest priority (soonest
    deadline) first."""
    return _sorted_by_priority(task_repository.query_by_pm(pm_id))


def list_projects(assigned_pm_id: int | None = None) -> list[dict]:
    """
    List of tasks (project_name, project_number, task_number, pm).
    If assigned_pm_id is given, only tasks claimed by that PM.
    If omitted, every task (admin view).
    """
    return task_repository.get_projects_rows(assigned_pm_id)


def list_distinct_projects(assigned_pm_id: int | None = None) -> list[dict]:
    """
    Distinct list of projects (project_number, project_name, pm), no duplicates
    from repeated tasks under the same project.
    If assigned_pm_id is given, only that PM's projects. If omitted, every project.
    """
    rows = task_repository.get_projects_rows(assigned_pm_id)

    seen = {}
    for row in rows:
        number = row.get("project_number")
        if number and number not in seen:
            seen[number] = {
                "project_number": number,
                "project_name": row.get("project_name"),
                "pm": row.get("pm"),
            }

    return sorted(seen.values(), key=lambda p: p["project_number"])


from datetime import date
from models.task import Task

def get_tasks_in_range(
    start_date: date,
    end_date: date | None = None,
    assigned_pm_id: int | None = None,
) -> list[Task]:
    """
    Tasks within a date range.
    - end_date omitted -> everything from start_date onward
    - assigned_pm_id given -> only that PM's tasks; omitted -> all tasks (admin view)
    """
    rows = task_repository.query_by_date_range(start_date, end_date, assigned_pm_id)
    return [Task(**row) for row in rows]