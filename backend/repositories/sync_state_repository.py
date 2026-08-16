from datetime import datetime

from repositories.supabase_client import get_supabase_client

TABLE = "sync_state"
SINGLETON_KEY = "mailbox_sync"


def get_last_synced_at() -> datetime | None:
    resp = (
        get_supabase_client()
        .table(TABLE)
        .select("last_synced_at")
        .eq("key", SINGLETON_KEY)
        .maybe_single()
        .execute()
    )
    if not resp or not resp.data:
        return None
    return datetime.fromisoformat(resp.data["last_synced_at"])


def set_last_synced_at(when: datetime) -> None:
    get_supabase_client().table(TABLE).upsert(
        {"key": SINGLETON_KEY, "last_synced_at": when.isoformat()}
    ).execute()
