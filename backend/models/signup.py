# backend/models/signup.py
from pydantic import BaseModel


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class SignupResponse(BaseModel):
    message: str