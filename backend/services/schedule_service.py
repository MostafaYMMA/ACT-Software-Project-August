# backend/services/schedule_service.py
from repositories import schedule_repository


def get_total_hours(resource: str, brand: str) -> float:
    """Total hours a resource has worked for a given brand."""
    rows = schedule_repository.get_hours_rows(resource=resource, brand=brand)
    return sum(row.get("hours_allocated") or 0 for row in rows)


def get_total_hours_by_rate_type(resource: str, rate_type: str) -> float:
    """Total hours a resource has worked under a given rate type."""
    rows = schedule_repository.get_hours_rows(resource=resource, rate_type=rate_type)
    return sum(row.get("hours_allocated") or 0 for row in rows)


def get_total_hours_by_location_type(resource: str, remote_or_onsite: str) -> float:
    rows = schedule_repository.get_hours_rows(resource=resource, remote_or_onsite=remote_or_onsite)
    return sum(row.get("hours_allocated") or 0 for row in rows)


def get_total_hours_by_country(resource: str, project_country: str) -> float:
    rows = schedule_repository.get_hours_rows(resource=resource, project_country=project_country)
    return sum(row.get("hours_allocated") or 0 for row in rows)