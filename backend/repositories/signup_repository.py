# backend/repositories/signup_repository.py
"""
Pure data access for creating a new Supabase Auth user. Kept in its own
file, separate from auth_repository.py (which the login flow depends on),
so signup work never touches anything login relies on.
"""
from supabase import create_client

from core.config import get_settings


def sign_up(email: str, password: str):
    """Create a new Supabase Auth user. Returns the raw auth response.

    Uses a throwaway client (never the shared get_supabase() singleton) —
    same reasoning as the one in auth_repository.py / /dev/login in main.py.
    """
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_key)
    return client.auth.sign_up({"email": email, "password": password})