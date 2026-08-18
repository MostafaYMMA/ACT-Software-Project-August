from fastapi import Depends, FastAPI

from api.v1.dependencies import get_current_pm
from api.v1.routers import pms, resources, schedule, sync, tasks
from models.pm import PM
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ACT Software Project - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",     # your local frontend dev URL
        "http://192.168.1.23:5173",  # frontend's LAN address, once you know it
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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