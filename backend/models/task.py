from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"


class ParsedTaskRow(BaseModel):
    """One task row extracted from an email table by services/parser.py."""

    title: str
    description: str | None = None
    assigned_pm_email: str | None = None
    due_date: datetime | None = None
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
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assigned_pm_id: int | None = None
    due_date: datetime | None = None


class TaskReassign(BaseModel):
    """Admin-only request body: move a task from whichever PM (or nobody)
    currently holds it to a different, specific PM."""

    new_pm_id: int

    
class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    assigned_pm_id: int | None = None
    source_email_id: str
    source_reference: str | None = None
    due_date: datetime | None = None
    created_at: datetime
    updated_at: datetime
