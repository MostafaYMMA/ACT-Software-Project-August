from repositories.supabase_client import get_supabase_client

TABLE = "pms"


def list_pms() -> list[dict]:
    resp = get_supabase_client().table(TABLE).select("*").execute()
    return resp.data


def get_pm_by_id(pm_id: str) -> dict | None:
    resp = get_supabase_client().table(TABLE).select("*").eq("id", pm_id).maybe_single().execute()
    return resp.data if resp else None


def get_pm_by_email(email: str) -> dict | None:
    resp = get_supabase_client().table(TABLE).select("*").eq("email", email).maybe_single().execute()
    return resp.data if resp else None
