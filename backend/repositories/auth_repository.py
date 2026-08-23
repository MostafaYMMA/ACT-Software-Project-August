# backend/repositories/auth_repository.py
"""
Repositories are pure data access — no business decisions (that's services/).

This one talks to Supabase Auth instead of a table. It always builds a
throwaway client (never the shared get_supabase() singleton in
supabase_client.py) because sign_in_with_password mutates the client
instance's own auth context — see the warning above /dev/login in main.py
for why that matters.
"""
from supabase import create_client

from core.config import get_settings


def _throwaway_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def sign_in(email: str, password: str):
    """Sign in with email/password. Returns the raw auth response."""
    client = _throwaway_client()
    return client.auth.sign_in_with_password({"email": email, "password": password})