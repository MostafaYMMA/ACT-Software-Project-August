from pydantic import BaseModel


class PM(BaseModel):
    id: str
    email: str
    name: str
