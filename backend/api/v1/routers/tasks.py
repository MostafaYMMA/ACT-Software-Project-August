from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependencies import get_current_pm, require_admin
from models.pm import PM
from services import task_service,pm_service
from models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def list_tasks(current_pm: PM = Depends(get_current_pm)):
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


@router.get("/projects")
def get_projects(assigned_pm_id: int | None = None) -> list[dict]:
    """
    GET /tasks/projects                     — all tasks (admin view)
    GET /tasks/projects?assigned_pm_id=5     — only tasks this PM has claimed
    """
    return task_service.list_projects(assigned_pm_id)