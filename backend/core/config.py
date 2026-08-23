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


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is only parsed once per process."""
    return Settings()


settings = get_settings()
