"""
One-off dev bootstrap: creates (or reuses) a Supabase Auth user plus its
matching `pms` row, so /dev/login has a real account to log in as.

Uses the service_role key (repositories.supabase_client.get_supabase), so it
bypasses the normal admin-only POST /pms flow — that's the point: there's no
existing admin to call it with on a fresh project.

Usage: python scripts/seed_dev_user.py
Reads DEV_TEST_USER_EMAIL / DEV_TEST_USER_PASSWORD from .env.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import settings
from repositories.supabase_client import get_supabase


def main() -> None:
    email = settings.dev_test_user_email
    password = settings.dev_test_user_password
    if not email or not password:
        raise SystemExit("Set DEV_TEST_USER_EMAIL / DEV_TEST_USER_PASSWORD in .env first.")

    supabase = get_supabase()

    existing = next(
        (u for u in supabase.auth.admin.list_users() if u.email == email),
        None,
    )
    if existing:
        auth_user = existing
        print(f"Auth user already exists: {email} ({auth_user.id})")
    else:
        created = supabase.auth.admin.create_user(
            {"email": email, "password": password, "email_confirm": True}
        )
        auth_user = created.user
        print(f"Created auth user: {email} ({auth_user.id})")

    pm_row = (
        supabase.table("pms")
        .select("*")
        .eq("auth_id", str(auth_user.id))
        .maybe_single()
        .execute()
    )
    if pm_row and pm_row.data:
        print(f"pms row already exists: id={pm_row.data['id']}")
        return

    inserted = (
        supabase.table("pms")
        .insert(
            {
                "email": email,
                "auth_id": str(auth_user.id),
                "name": "Dev Test PM",
                "is_admin": True,
            }
        )
        .execute()
    )
    print(f"Created pms row: {inserted.data}")


if __name__ == "__main__":
    main()
