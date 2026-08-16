"""
One-off sanity check — run this after setting up .env to confirm the
Supabase connection works before building anything on top of it.

    python check_supabase_connection.py
"""

from repositories.supabase_client import get_supabase


def main() -> None:
    supabase = get_supabase()
    # Swap "tasks" for any table name that exists in your project once you've
    # created one; this just confirms the client can reach your project.
    response = supabase.table("supplier_schedule").select("*").limit(1).execute()
    print("Connected. Sample response data:", response.data)


if __name__ == "__main__":
    main()