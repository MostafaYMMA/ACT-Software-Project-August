from datetime import datetime,date
from enum import Enum
from typing import Optional


from pydantic import BaseModel


class TaskStatus(str, Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"


class ParsedTaskRow(BaseModel):
    """One task row extracted from an email table by services/parser.py."""

    title: str
    description: str | None = None
    assigned_pm_email: str | None = None
    # TODO(open decision): whichever field the team picks as the dedupe key
    # for overwrite matching should be added here once confirmed.
    source_reference: str | None = None
    

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus
    assigned_pm_id: int | None = None
    source_email_id: str
    source_reference: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assigned_pm_id: int | None = None


class TaskReassign(BaseModel):
    """Admin-only request body: move a task from whichever PM (or nobody)
    currently holds it to a different, specific PM."""

    new_pm_id: int

    
class Task(BaseModel):
    id: int
    supplier_name: Optional[str] = None
    resource: Optional[str] = None
    resource_start: Optional[datetime] = None
    resource_end: Optional[datetime] = None
    hours_allocated: Optional[float] = None
    project_number: Optional[str] = None
    project_name: Optional[str] = None
    task_number: Optional[str] = None
    pm: Optional[str] = None
    resource_manager: Optional[str] = None
    project_status: Optional[str] = None
    project_country: Optional[str] = None
    remote_onsite: Optional[str] = None
    brand: Optional[str] = None
    po: Optional[str] = None
    sow: Optional[str] = None
    rate_type: Optional[str] = None