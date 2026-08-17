from fastapi import Depends, FastAPI

from api.v1.dependencies import get_current_pm
from api.v1.routers import pms, resources, schedule, sync, tasks
from models.pm import PM


app = FastAPI(title="ACT Software Project - Backend")

app.include_router(tasks.router, prefix="/api/v1")
app.include_router(pms.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")
app.include_router(schedule.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me")
async def me(pm: PM = Depends(get_current_pm)) -> PM:
    return pm