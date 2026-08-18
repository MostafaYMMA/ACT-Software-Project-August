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