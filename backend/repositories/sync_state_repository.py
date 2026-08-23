from datetime import datetime

from repositories.supabase_client import get_supabase

TABLE = "tasks"


def get_last_synced_at() -> datetime | None:
    """Derived from the data itself instead of a dedicated sync_state row -
    the most recent created_at in `tasks` stands in for "last synced at".
    Approximate: anything else that writes to `tasks` also shifts this.
    """
    resp = (
        get_supabase()
        .table(TABLE)
        .select("created_at")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    return datetime.fromisoformat(resp.data[0]["created_at"])


def set_last_synced_at(when: datetime) -> None:
    """No-op - the timestamp is implicit in tasks.created_at, there's
    nothing separate to write."""
