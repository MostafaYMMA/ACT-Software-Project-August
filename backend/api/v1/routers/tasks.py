from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependencies import get_current_pm
from models.pm import PM
from services import task_service

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
