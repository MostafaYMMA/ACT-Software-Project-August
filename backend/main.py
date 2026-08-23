from fastapi import Depends, FastAPI, Form, HTTPException
from supabase import create_client

from api.v1.dependencies import get_current_pm
from api.v1.routers import auth, pms, schedule, sync, tasks
from api.v1.routers import signup as signup_router
from core.config import settings
from models.pm import PM
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ACT Software Project - Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this later once frontend has a real domain
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(tasks.router, prefix="/api/v1")
app.include_router(pms.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")
app.include_router(schedule.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(signup_router.router, prefix="/api/v1")

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
#
# IMPORTANT: sign_in_with_password() mutates the client instance's own auth
# context (swaps its Authorization header from the service_role key to the
# logged-in user's session token). repositories.supabase_client.get_supabase()
# is an lru_cache'd singleton shared by every request in this worker, so
# calling sign_in_with_password() on it would silently downgrade every other
# request in the process from service_role to that user's RLS-scoped session.
# Use a throwaway client here instead — never the shared one.
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

    throwaway_client = create_client(settings.supabase_url, settings.supabase_key)
    try:
        auth_response = throwaway_client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    except Exception as exc:  # supabase raises its own AuthApiError subclasses
        raise HTTPException(status_code=401, detail="Invalid credentials") from exc

    return {"access_token": auth_response.session.access_token, "token_type": "bearer"}
