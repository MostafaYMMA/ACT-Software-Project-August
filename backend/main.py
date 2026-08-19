
# dont remove this
# python -m http.server 8765 --directory "frontend (2)"
# http://127.0.0.1:8765/

from fastapi import Depends, FastAPI

from api.v1.dependencies import get_current_pm
from api.v1.routers import pms, sync, tasks
from models.pm import PM

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
