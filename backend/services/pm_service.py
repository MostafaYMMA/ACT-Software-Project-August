from repositories import pm_repository


def list_pms() -> list[dict]:
    return pm_repository.list_pms()


def get_pm(pm_id: str) -> dict | None:
    return pm_repository.get_pm_by_id(pm_id)
