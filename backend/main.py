from fastapi import Depends, FastAPI

from api.v1.dependencies import get_current_pm
from models.pm import PM

app = FastAPI(title="ACT Software Project - Backend")


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running"}


# TODO(Adam, Slice 5): throwaway endpoint to prove the auth chain end-to-end.
# Remove once Kassem/Ali/Mostafa have wired get_current_pm/require_admin
# into their own routers.
@app.get("/me")
async def me(pm: PM = Depends(get_current_pm)) -> PM:
    return pm