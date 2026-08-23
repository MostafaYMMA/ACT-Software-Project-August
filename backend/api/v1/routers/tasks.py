from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependencies import get_current_pm, require_admin
from models.pm import PM
from models.task import Task, TaskReassign
from services import task_service, pm_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


# --- literal/specific paths first ---

@router.get("")
def list_tasks(current_pm: PM = Depends(get_current_pm)):
    return task_service.list_tasks()


@router.get("/projects")
def get_projects(
    assigned_pm_id: int | None = None, current_pm: PM = Depends(get_current_pm)
) -> list[dict]:
    """
    GET /tasks/projects                     — all tasks (admin view)
    GET /tasks/projects?assigned_pm_id=5     — only tasks this PM has claimed
    """
    return task_service.list_projects(assigned_pm_id)


@router.get("/projects/distinct")
def get_distinct_projects(assigned_pm_id: int | None = None) -> list[dict]:
    """
    GET /tasks/projects/distinct                    — all distinct projects (admin view)
    GET /tasks/projects/distinct?assigned_pm_id=5    — only this PM's distinct projects
    """
    return task_service.list_distinct_projects(assigned_pm_id)


@router.get("/range", response_model=list[Task])
def get_tasks_in_range(
    start_date: date,
    end_date: date | None = None,
    assigned_pm_id: int | None = None,
):
    """
    GET /tasks/range?start_date=2026-08-01
        -> all tasks from this date onward, every PM (admin view)
    GET /tasks/range?start_date=2026-08-01&end_date=2026-08-17
        -> all tasks within this range, every PM
    GET /tasks/range?start_date=2026-08-01&assigned_pm_id=5
        -> only this PM's tasks, from this date onward
    """
    return task_service.get_tasks_in_range(start_date, end_date, assigned_pm_id)


# --- everything below has a {path_param} and must stay last ---

@router.get("/{task_id}")
def get_task(task_id: int, current_pm: PM = Depends(get_current_pm)):
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/{task_id}/claim")
def claim_task(task_id: int, current_pm: PM = Depends(get_current_pm)):
    try:
        return task_service.claim_task(task_id, current_pm.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_pm: PM = Depends(require_admin)):
    try:
        task_service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{task_id}/unassign")
def unassign_task(task_id: int, current_pm: PM = Depends(get_current_pm)):
    try:
        return task_service.unassign_task(task_id, current_pm)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.patch("/{task_id}/reassign")
def reassign_task(task_id: int, body: TaskReassign, current_pm: PM = Depends(require_admin)):
    """Admin-only: transfer a task from whichever PM (or nobody) currently
    holds it to a different PM specified by body.new_pm_id."""
    try:
        return task_service.reassign_task(task_id, body.new_pm_id, current_pm)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/{pm_id}/tasks")
def get_pm_tasks(pm_id: int, current_pm: PM = Depends(get_current_pm)) -> list[dict]:
    """GET /pms/{pm_id}/tasks — return all tasks assigned to this PM."""
    pm_service.get_pm(pm_id)  # confirms PM exists, raises 404 if not
    return task_service.get_tasks_for_pm(pm_id)