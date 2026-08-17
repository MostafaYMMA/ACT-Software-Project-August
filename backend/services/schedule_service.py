# backend/services/schedule_service.py
from repositories import schedule_repository

ALLOWED_ATTRIBUTES = {"brand", "rate_type", "project_country", "remote_or_onsite"}



# backend/services/schedule_service.py

ALLOWED_ATTRIBUTES = {
    "brand",
    "rate_type",
    "project_country",
    "remote_or_onsite",
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