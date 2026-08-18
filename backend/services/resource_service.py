from repositories import resource_repository


def list_resources() -> list[str]:
    """Return unique, non-empty resource names."""
    rows = resource_repository.list_resource_rows()

    resources = {
        row["resource"].strip()
        for row in rows
        if row.get("resource") and row["resource"].strip()
    }

    return sorted(resources, key=str.casefold)


def get_resource_details(resource_name: str) -> list[dict]:
    """Return every schedule row belonging to the selected resource."""
    normalized_name = resource_name.strip()

    if not normalized_name:
        return []

    return resource_repository.get_rows_by_resource(normalized_name)

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


def list_resources_by_attributes(**attribute_filters: str) -> list[str]:
    """
    Return unique, non-empty resource names, filtered by any number of attributes.
    attribute_filters example: {"brand": "IHG", "rate_type": "Hourly"}
    """
    invalid = set(attribute_filters) - ALLOWED_ATTRIBUTES
    if invalid:
        raise ValueError(f"Invalid attribute(s): {invalid}. Must be one of {ALLOWED_ATTRIBUTES}")

    rows = resource_repository.get_rows_by_attributes(**attribute_filters)

    resources = {
        row["resource"].strip()
        for row in rows
        if row.get("resource") and row["resource"].strip()
    }

    return sorted(resources, key=str.casefold)