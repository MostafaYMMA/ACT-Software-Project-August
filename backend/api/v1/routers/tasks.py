from fastapi import APIRouter, Depends, HTTPException, status, Query

from api.v1.dependencies import get_current_pm, require_admin
from models.pm import PM
from services import task_service,pm_service
from models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def list_tasks(
    current_pm: PM = Depends(get_current_pm),
    search: str | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    status: str | None = Query(None),
):
    """
    List all tasks with optional search and date filters.
    
    Query parameters:
    - search: Text to search in task title, description, source_reference
    - from_date: Filter tasks created on or after this date (YYYY-MM-DD)
    - to_date: Filter tasks created on or before this date (YYYY-MM-DD)
    - status: Filter by status ('assigned' or 'unassigned')
    
    Example: GET /api/v1/tasks?search=onboarding&from_date=2026-08-01&to_date=2026-08-18
    """
    if search or from_date or to_date or status:
        return task_service.search_tasks(search, from_date, to_date, status)
    return task_service.list_tasks()


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

@router.get("/{pm_id}/tasks", response_model=list[Task])
def get_pm_tasks(pm_id: int):
    """GET /pms/{pm_id}/tasks — return all tasks assigned to this PM."""
    pm_service.get_pm(pm_id)  # confirms PM exists, raises 404 if not
    return task_service.get_tasks_for_pm(pm_id)