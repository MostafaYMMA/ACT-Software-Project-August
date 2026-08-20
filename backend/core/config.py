from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central place for all env-var config. Nothing outside core/ should
    call os.environ directly — import get_settings() instead.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- Supabase ---
    supabase_url: str
    supabase_key: str  # service_role key — backend only, never ship to a client/browser

    # --- Supabase Auth (JWT verification) ---
    supabase_jwt_secret: str | None = None

    # --- Environment ---
    environment: str = "development"  # "production" disables /dev/login

    # --- Dev-only test login (Swagger convenience, see /dev/login) ---
    dev_test_user_email: str | None = None
    dev_test_user_password: str | None = None

    # --- Microsoft Graph (app-only auth against the shared mailbox) ---
    ms_tenant_id: str | None = None
    ms_client_id: str | None = None
    ms_client_secret: str | None = None
    ms_mailbox_user: str | None = None  # UPN/address of the shared mailbox


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is only parsed once per process."""
    return Settings()


settings = get_settings()
