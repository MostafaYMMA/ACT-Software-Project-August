# backend/api/v1/routers/schedule.py
from fastapi import APIRouter
from services import schedule_service

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/hours")
def get_resource_hours(resource: str, brand: str) -> float:
    """GET /schedule/hours?resource=...&brand=... — total hours worked."""
    return schedule_service.get_total_hours(resource, brand)

@router.get("/hours/by-rate-type")
def get_resource_hours_by_rate_type(resource: str, rate_type: str) -> float:
    """GET /schedule/hours/by-rate-type?resource=...&rate_type=Hourly"""
    return schedule_service.get_total_hours_by_rate_type(resource, rate_type)

@router.get("/hours/by-country")
def get_resource_hours_by_country(resource: str, project_country: str) -> float:
    """GET /schedule/hours/by-country?resource=...&project_country=..."""
    return schedule_service.get_total_hours_by_country(resource, project_country)


@router.get("/hours/by-location-type")
def get_resource_hours_by_location_type(resource: str, remote_or_onsite: str) -> float:
    """GET /schedule/hours/by-location-type?resource=...&remote_or_onsite=..."""
    return schedule_service.get_total_hours_by_location_type(resource, remote_or_onsite)