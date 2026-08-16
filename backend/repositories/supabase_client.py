from functools import lru_cache

from supabase import Client, create_client

from core.config import get_settings


@lru_cache
def get_supabase() -> Client:
    """
    Returns a cached Supabase client (one per process).

    This is the ONLY place in the codebase allowed to construct a Supabase
    client. Every other file in repositories/ should import get_supabase()
    from here rather than calling create_client() itself — that keeps the
    "repositories/ is the only layer that talks to Supabase" rule enforceable
    in one spot.
    """
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)
