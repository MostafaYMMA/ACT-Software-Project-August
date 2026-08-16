from fastapi import FastAPI

from api.v1.routers import pms, sync, tasks

app = FastAPI(title="Task Ingestion API")

app.include_router(tasks.router, prefix="/api/v1")
app.include_router(pms.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
