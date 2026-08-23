from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum



class ProjectStatus(str, Enum):
    ACTIVE = "Active"
    POST_WAR = "Post-WAR"
    PENDING = "Pending"
    NOT_ACTIVE = "Not-Active"

class ProjectStatusUpdate(BaseModel):
    project_status: ProjectStatus
class SupplierSchedule(BaseModel):
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
    