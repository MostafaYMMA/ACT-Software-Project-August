from fastapi import Depends, FastAPI, Form, HTTPException

from api.v1.dependencies import get_current_pm
from api.v1.routers import pms, sync, tasks
from core.config import settings
from models.pm import PM
from repositories.supabase_client import get_supabase

app = FastAPI(title="ACT Software Project - Backend")

app.include_router(tasks.router, prefix="/api/v1")
app.include_router(pms.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# TODO(Adam, Slice 5): throwaway endpoint to prove the auth chain end-to-end.
# Remove once Kassem/Ali/Mostafa have wired get_current_pm/require_admin
# into their own routers.
@app.get("/me")
async def me(pm: PM = Depends(get_current_pm)) -> PM:
    return pm


# TODO(Adam): dev-only token endpoint wired as an OAuth2 "password" flow so
# Swagger's Authorize button renders a login form instead of requiring a
# manually-copied token. Leave username/password blank in that form and it
# logs in as the seeded test PM (DEV_TEST_USER_EMAIL / DEV_TEST_USER_PASSWORD
# in .env). Disabled whenever ENVIRONMENT=production. Never expose in prod.
@app.post("/dev/login")
def dev_login(
    username: str | None = Form(None),
    password: str | None = Form(None),
) -> dict:
    if settings.environment == "production":
        raise HTTPException(status_code=404, detail="Not found")

    email = username or settings.dev_test_user_email
    password = password or settings.dev_test_user_password
    if not email or not password:
        raise HTTPException(
            status_code=500,
            detail="DEV_TEST_USER_EMAIL / DEV_TEST_USER_PASSWORD not set in .env",
        )

    try:
        auth_response = get_supabase().auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    except Exception as exc:  # supabase raises its own AuthApiError subclasses
        raise HTTPException(status_code=401, detail="Invalid credentials") from exc

    return {"access_token": auth_response.session.access_token, "token_type": "bearer"}
