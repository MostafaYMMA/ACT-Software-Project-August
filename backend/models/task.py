from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"


class TaskFields(BaseModel):
    """The columns carried over verbatim from the supplier-schedule table in
    each email (one table row -> one task). Field names mirror the incoming
    Excel/email columns:

    supplier name, resource, resource start, resource end, hours allocated,
    project_number, project_name, task_number, pm, resource manager,
    project_status, project_country, remote_onsite, brand, po, sow, rate_type
    """

    supplier_name: str
    resource: str
    resource_start: date
    resource_end: date
    hours_allocated: float
    project_number: str
    project_name: str | None = None
    task_number: str
    pm: str | None = None
    resource_manager: str | None = None
    project_status: str | None = None
    project_country: str | None = None
    remote_onsite: str | None = None
    brand: str | None = None
    po: str | None = None
    sow: str | None = None
    rate_type: str | None = None


class ParsedTaskRow(TaskFields):
    """One row extracted from an email table by services/parser.py."""


class TaskCreate(TaskFields):
    status: TaskStatus
    assigned_pm_id: int | None = None
    source_email_id: str


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    assigned_pm_id: int | None = None
    # Any TaskFields column can also be corrected via a full row overwrite;
    # this model is for the assign/claim-style partial updates only.


class Task(TaskFields):
    id: int
    status: TaskStatus
    assigned_pm_id: int | None = None
    source_email_id: str
    created_at: datetime
    updated_at: datetime
