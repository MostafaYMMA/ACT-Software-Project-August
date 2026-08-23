# backend/services/schedule_service.py
from repositories import schedule_repository





ALLOWED_ATTRIBUTES = {
    "brand",
    "rate_type",
    "project_country",
    "remote_onsite",
    "project_number",
    "project_name",
    "pm",
    "resource_manager",
}


def get_total_hours_dynamic(resource: str, **attribute_filters: str) -> float:
    """
    Total hours for a resource, filtered by any number of attributes.
    attribute_filters example: {"brand": "IHG", "rate_type": "Hourly"}
    """
    invalid = set(attribute_filters) - ALLOWED_ATTRIBUTES
    if invalid:
        raise ValueError(f"Invalid attribute(s): {invalid}. Must be one of {ALLOWED_ATTRIBUTES}")

    rows = schedule_repository.get_hours_rows(resource=resource, **attribute_filters)
    return sum(row.get("hours_allocated") or 0 for row in rows)

def update_project_status(project_number: str, current_pm, new_status: str) -> list[dict]:
    project_number = (project_number or "").strip()
    if not project_number:
        raise ValueError("project_number is required")

    rows = schedule_repository.get_rows_by_project_number(project_number)
    if not rows:
        raise ValueError("Project not found")

    if current_pm.is_admin:
        updated = schedule_repository.update_project_status(project_number, new_status)
    else:
        updated = schedule_repository.update_project_status(
            project_number, new_status, pm_name=current_pm.name
        )
        if not updated:
            raise PermissionError("You can only update the status of your own projects")

    return updated